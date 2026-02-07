from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from decimal import Decimal

from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.denomination import Denomination
from app.models.purchase_denomination import PurchaseDenomination
from app.schemas.schemas import PurchaseCreate, PurchaseItemInput
from app.core.exceptions import (
    ResourceNotFoundException,
    InsufficientStockException,
    InvalidPaymentException,
    InsufficientDenominationException
)
from app.utils.denomination_calculator import calculate_change_denominations
import logging

logger = logging.getLogger(__name__)


class BillingService:
    """
    Production-grade billing service with ACID transaction management.
    Follows the exact data flow: Customer -> Purchase -> PurchaseItems -> Stock Update -> Denominations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_purchase(self, purchase_data: PurchaseCreate) -> Purchase:
        """
        Create a complete purchase with full transaction management.
        
        Transaction Flow:
        1. Get or create customer
        2. Validate products and stock
        3. Calculate totals
        4. Create purchase record
        5. Create purchase items with snapshots
        6. Update product stock
        7. Handle change denominations
        8. Commit or rollback
        """
        try:
            # Step 1: Get or create customer
            customer = self._get_or_create_customer(purchase_data.customer_email)
            
            # Step 2: Validate products and stock
            products_data = self._validate_and_fetch_products(purchase_data.items)
            
            # Step 3: Calculate totals
            calculations = self._calculate_purchase_totals(products_data)
            
            # Step 4: Validate payment
            if purchase_data.paid_amount < calculations['final_amount']:
                raise InvalidPaymentException(
                    f"Insufficient payment. Required: {calculations['final_amount']}, Paid: {purchase_data.paid_amount}"
                )
            
            # Step 5: Create purchase record
            purchase = Purchase(
                customer_id=customer.id,
                total_amount=calculations['total_amount'],
                tax_amount=calculations['tax_amount'],
                final_amount=calculations['final_amount'],
                paid_amount=purchase_data.paid_amount,
                balance_amount=purchase_data.paid_amount - calculations['final_amount']
            )
            self.db.add(purchase)
            self.db.flush()  # Get purchase.id without committing
            
            # Step 6: Create purchase items with price snapshots
            self._create_purchase_items(purchase.id, products_data)
            
            # Step 7: Update product stock (CRITICAL - inventory management)
            self._update_product_stock(products_data)
            
            # Step 8: Handle change denominations
            change_amount = purchase_data.paid_amount - calculations['final_amount']
            if change_amount > 0:
                self._handle_change_denominations(purchase.id, change_amount)
            
            # Commit transaction
            self.db.commit()
            self.db.refresh(purchase)
            
            logger.info(f"Purchase {purchase.id} created successfully for customer {customer.email}")
            return purchase
            
        except (ResourceNotFoundException, InsufficientStockException, 
                InvalidPaymentException, InsufficientDenominationException) as e:
            self.db.rollback()
            logger.error(f"Business rule violation: {e.message}")
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during purchase creation: {str(e)}")
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Unexpected error during purchase creation: {str(e)}")
            raise
    
    def _get_or_create_customer(self, email: str) -> Customer:
        """Get existing customer or create new one"""
        customer = self.db.query(Customer).filter(Customer.email == email).first()
        if not customer:
            customer = Customer(email=email)
            self.db.add(customer)
            self.db.flush()
            logger.info(f"New customer created: {email}")
        return customer
    
    def _validate_and_fetch_products(self, items: List[PurchaseItemInput]) -> List[Dict]:
        """Validate products exist and have sufficient stock"""
        products_data = []
        
        for item in items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            
            if not product:
                raise ResourceNotFoundException(
                    f"Product with ID {item.product_id} not found"
                )
            
            if product.stock < item.quantity:
                raise InsufficientStockException(
                    f"Insufficient stock for {product.name}. Available: {product.stock}, Required: {item.quantity}"
                )
            
            products_data.append({
                'product': product,
                'quantity': item.quantity
            })
        
        return products_data
    
    def _calculate_purchase_totals(self, products_data: List[Dict]) -> Dict[str, float]:
        """Calculate total amount, tax, and final amount"""
        total_amount = 0.0
        total_tax = 0.0
        
        for data in products_data:
            product = data['product']
            quantity = data['quantity']
            
            item_total = product.price * quantity
            item_tax = item_total * (product.tax_percent / 100)
            
            total_amount += item_total
            total_tax += item_tax
            
            # Store calculated values for later use
            data['item_total'] = item_total
            data['item_tax'] = item_tax
        
        final_amount = total_amount + total_tax
        
        return {
            'total_amount': round(total_amount, 2),
            'tax_amount': round(total_tax, 2),
            'final_amount': round(final_amount, 2)
        }
    
    def _create_purchase_items(self, purchase_id: int, products_data: List[Dict]):
        """Create purchase items with price snapshots (NEVER recompute history)"""
        for data in products_data:
            product = data['product']
            quantity = data['quantity']
            
            purchase_item = PurchaseItem(
                purchase_id=purchase_id,
                product_id=product.id,
                quantity=quantity,
                unit_price_snapshot=product.price,  # Freeze current price
                tax_percent_snapshot=product.tax_percent,  # Freeze current tax
                tax_amount=round(data['item_tax'], 2),
                total_price=round(data['item_total'] + data['item_tax'], 2)
            )
            self.db.add(purchase_item)
    
    def _update_product_stock(self, products_data: List[Dict]):
        """Update product inventory"""
        for data in products_data:
            product = data['product']
            quantity = data['quantity']
            product.stock -= quantity
            logger.debug(f"Stock updated for {product.name}: {product.stock + quantity} -> {product.stock}")
    
    def _handle_change_denominations(self, purchase_id: int, change_amount: float):
        """Calculate and store change denominations"""
        # Fetch available denominations
        denominations = self.db.query(Denomination).all()
        available_denoms = {d.value: d.available_count for d in denominations}
        
        # Calculate optimal change breakdown
        change_breakdown = calculate_change_denominations(change_amount, available_denoms)
        
        # Store change given and update denomination stock
        for denom_value, count in change_breakdown.items():
            # Record change given
            purchase_denom = PurchaseDenomination(
                purchase_id=purchase_id,
                denomination_value=denom_value,
                count_given=count
            )
            self.db.add(purchase_denom)
            
            # Update denomination stock
            denom = self.db.query(Denomination).filter(Denomination.value == denom_value).first()
            denom.available_count -= count
            
        logger.info(f"Change of {change_amount} given using denominations: {change_breakdown}")
