# 🧾 Billing System - Production Grade FastAPI Application

A complete billing system with web UI, automatic email invoicing, and ACID transaction management.

## ✨ Features Implemented

✅ **All Requirements from Screenshots:**
1. Product management with database schema
2. Billing calculation page (Page 1)
3. Customer email input
4. Dynamic "Add New" button for products
5. Product ID and Quantity fields
6. Denominations section (500, 50, 20, 10, 5, 2, 1)
7. Cash paid by customer input
8. "Generate Bill" button with calculations (Page 2)
9. Automatic email sending (asynchronous)
10. Balance denomination calculation
11. Purchase history view
12. Purchase details view

✅ **Additional Production Features:**
- ACID transaction management
- Price snapshots (historical accuracy)
- Automatic inventory updates
- Clean architecture (Repository → Service → Router)
- Error handling with proper HTTP codes
- Connection pooling
- Comprehensive logging

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Server
```bash
uvicorn app.main:app --reload
```

### 3. Add Sample Products
**In a new terminal:**
```bash
python add_sample_products.py
```

### 4. Access Application
- **Billing Page**: http://127.0.0.1:8000/
- **Purchase History**: http://127.0.0.1:8000/purchases
- **API Documentation**: http://127.0.0.1:8000/docs

## 📖 How to Use the Billing System

### Creating a Bill (Page 1)

1. **Enter Customer Email**
   ```
   customer@example.com
   ```

2. **Add Products to Bill**
   - Enter Product ID (1, 2, 3, etc.)
   - Enter Quantity
   - Click "Add New" to add more products
   - Click "Remove" to delete a product row

3. **Denominations** (Auto-setup)
   - System automatically creates denominations with 100 count each
   - Values: 500, 50, 20, 10, 5, 2, 1
   - Modify counts if needed

4. **Enter Cash Paid**
   ```
   Amount: 130000
   ```

5. **Generate Bill**
   - Click "Generate Bill" button
   - System performs:
     - ✅ Customer validation/creation
     - ✅ Product validation & stock check
     - ✅ Total calculation with tax
     - ✅ Purchase record creation
     - ✅ Price snapshot storage
     - ✅ Inventory update
     - ✅ Change calculation
     - ✅ Email sending (async)

### Viewing Invoice (Page 2)

After clicking "Generate Bill", you'll see:

**Bill Section:**
| Product ID | Unit Price | Quantity | Purchase Price | Tax % | Tax Amount | Total |
|------------|------------|----------|----------------|-------|------------|-------|
| 1          | 80000.00   | 1        | 80000.00       | 18%   | 14400.00   | 94400.00 |
| 2          | 15000.00   | 2        | 30000.00       | 12%   | 3600.00    | 33600.00 |

**Totals:**
- Total price without tax: ₹110,000.00
- Total tax payable: ₹18,000.00
- Net price: ₹128,000.00
- Paid amount: ₹130,000.00
- Balance payable to customer: ₹2,000.00

**Balance Denomination:**
- 500: 4

### Viewing Purchase History

1. Click "View Purchase History" link
2. See all purchases in a table
3. Click any row to view purchase details
4. See items purchased in that transaction

## 📧 Email Configuration

Email invoices are sent automatically after bill generation.

**To enable email sending:**

1. Edit `app/services/email_service.py`
2. Uncomment lines 30-33
3. Add SMTP credentials:

```python
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

**For Gmail:**
- Enable 2-Factor Authentication
- Generate App Password: https://myaccount.google.com/apppasswords
- Use app password in code

**Email contains:**
- Invoice number
- Purchase date
- Items table with prices and tax
- Total calculations
- Change denominations

## 🎯 API Endpoints

### Products
```
POST   /api/v1/products          Create product
GET    /api/v1/products          List all products
GET    /api/v1/products/{id}     Get product by ID
PUT    /api/v1/products/{id}     Update product
DELETE /api/v1/products/{id}     Delete product
```

### Denominations
```
POST   /api/v1/denominations           Create denomination
GET    /api/v1/denominations           List all denominations
PUT    /api/v1/denominations/{value}   Update denomination count
```

### Purchases (Billing)
```
POST   /api/v1/purchases          Create purchase (Generate Bill)
GET    /api/v1/purchases          List all purchases
GET    /api/v1/purchases/{id}     Get purchase details
```

### UI Pages
```
GET    /                          Billing page
GET    /purchases                 Purchase history page
```

## 📊 Database Schema

```sql
-- Customer table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP
);

-- Product table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    price FLOAT NOT NULL CHECK (price > 0),
    tax_percent FLOAT NOT NULL CHECK (tax_percent >= 0),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Purchase table
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    total_amount FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    final_amount FLOAT NOT NULL,
    paid_amount FLOAT NOT NULL,
    balance_amount FLOAT NOT NULL,
    created_at TIMESTAMP
);

-- Purchase items with price snapshots
CREATE TABLE purchase_items (
    id INTEGER PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price_snapshot FLOAT NOT NULL,
    tax_percent_snapshot FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    total_price FLOAT NOT NULL
);

-- Denominations
CREATE TABLE denominations (
    id INTEGER PRIMARY KEY,
    value INTEGER UNIQUE NOT NULL,
    available_count INTEGER NOT NULL CHECK (available_count >= 0),
    updated_at TIMESTAMP
);

-- Change given tracking
CREATE TABLE purchase_denominations (
    id INTEGER PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id),
    denomination_value INTEGER NOT NULL,
    count_given INTEGER NOT NULL
);
```

## 🏗️ Project Structure

```
billing-fastapi/
├── app/
│   ├── core/                    # Configuration & exceptions
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── db/                      # Database setup
│   │   └── database.py
│   ├── models/                  # SQLAlchemy models
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── purchase.py
│   │   ├── purchase_item.py
│   │   ├── denomination.py
│   │   └── purchase_denomination.py
│   ├── schemas/                 # Pydantic schemas
│   │   └── schemas.py
│   ├── crud/                    # Repository pattern
│   │   ├── product_repository.py
│   │   ├── denomination_repository.py
│   │   └── purchase_repository.py
│   ├── services/                # Business logic
│   │   ├── billing_service.py
│   │   └── email_service.py
│   ├── routers/                 # API endpoints
│   │   ├── product_router.py
│   │   ├── purchase_router.py
│   │   ├── denomination_router.py
│   │   └── ui_router.py
│   ├── templates/               # HTML pages
│   │   ├── billing.html
│   │   └── purchases.html
│   ├── utils/                   # Helper functions
│   │   └── denomination_calculator.py
│   └── main.py                  # Application entry point
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── add_sample_products.py       # Sample data script
├── SETUP_GUIDE.md              # Detailed setup guide
└── README.md                    # This file
```

## 🔥 Example Usage

### 1. Add Products (via API)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "stock": 10,
    "price": 80000,
    "tax_percent": 18
  }'
```

### 2. Create Purchase (via UI)
1. Open http://127.0.0.1:8000/
2. Enter email: `customer@example.com`
3. Add products: Product ID `1`, Quantity `1`
4. Enter paid amount: `100000`
5. Click "Generate Bill"

### 3. View History
- Visit http://127.0.0.1:8000/purchases
- Click any purchase to see details

## 🎨 UI Features

- **Clean Design**: Simple, professional interface
- **Responsive**: Works on desktop and mobile
- **Dynamic Forms**: Add/remove product rows
- **Real-time Display**: Invoice shown immediately
- **Error Handling**: User-friendly error messages
- **Purchase History**: View all past transactions

## 🔒 Production Best Practices

1. **ACID Transactions**: All-or-nothing database operations
2. **Price Snapshots**: Historical data never changes
3. **Async Email**: Non-blocking email sending
4. **Connection Pooling**: Efficient database connections
5. **Error Handling**: Proper HTTP status codes
6. **Logging**: Comprehensive logging for debugging
7. **Validation**: Pydantic schemas for data validation
8. **Repository Pattern**: Clean separation of concerns

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

**Products not found:**
```bash
# Add sample products
python add_sample_products.py
```

**Email not sending:**
- Configure SMTP credentials in `email_service.py`
- Check logs for error messages

**Database errors:**
- Check `.env` file for correct DATABASE_URL
- Delete `billing.db` and restart to recreate

## 📝 Notes

- System uses SQLite by default (no setup needed)
- Denominations auto-created with 100 count each
- Email sending is asynchronous (doesn't block)
- Stock automatically updated on purchase
- Price snapshots ensure historical accuracy
- All operations wrapped in ACID transactions

## 🚀 Deployment

For production deployment:

1. **Use PostgreSQL**:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/billing_db
   ```

2. **Configure Email**:
   - Add SMTP credentials
   - Use environment variables

3. **Run with Gunicorn**:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Add HTTPS**:
   - Use Nginx/Traefik as reverse proxy
   - Configure SSL certificates

## 📄 License

MIT License - Feel free to use for any purpose

---

**Built with ❤️ using FastAPI, SQLAlchemy, and vanilla JavaScript**

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
