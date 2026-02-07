# Billing System - Setup & Usage Guide

## ✅ Features Implemented

1. ✅ Product management with CRUD operations
2. ✅ Billing calculation page with dynamic product rows
3. ✅ Denomination management (500, 50, 20, 10, 5, 2, 1)
4. ✅ Automatic change calculation
5. ✅ Email invoice sending (asynchronous)
6. ✅ Purchase history view
7. ✅ Simple, clean UI
8. ✅ ACID transaction management
9. ✅ Price snapshots for historical accuracy

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
The system uses SQLite by default (no setup needed).

For PostgreSQL:
```env
# Edit .env file
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/billing_db
```

### 3. Add Sample Products
```bash
# Run this Python script to add test products
python -c "
import requests
API = 'http://127.0.0.1:8000/api/v1'

products = [
    {'name': 'iPhone 15', 'stock': 10, 'price': 80000, 'tax_percent': 18},
    {'name': 'AirPods Pro', 'stock': 20, 'price': 15000, 'tax_percent': 12},
    {'name': 'MacBook Pro', 'stock': 5, 'price': 150000, 'tax_percent': 18}
]

for p in products:
    r = requests.post(f'{API}/products', json=p)
    print(f'Created: {r.json()}')
"
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```

### 5. Access Application
- **Billing Page**: http://127.0.0.1:8000/
- **Purchase History**: http://127.0.0.1:8000/purchases
- **API Docs**: http://127.0.0.1:8000/docs

## 📖 How to Use

### Creating a Bill

1. **Enter Customer Email**
   - Type customer email (e.g., customer@example.com)

2. **Add Products**
   - Enter Product ID (1, 2, 3, etc.)
   - Enter Quantity
   - Click "Add New" for more products
   - Click "Remove" to delete a row

3. **Set Denominations** (Optional)
   - System auto-creates denominations with 100 count each
   - Modify counts if needed

4. **Enter Paid Amount**
   - Enter cash paid by customer

5. **Generate Bill**
   - Click "Generate Bill"
   - System will:
     - Validate products and stock
     - Calculate totals with tax
     - Calculate change denominations
     - Create purchase record
     - Update inventory
     - Send email invoice (async)
     - Display invoice on screen

### Viewing Purchase History

1. Click "View Purchase History" link
2. Click any row to see purchase details
3. View items purchased in that transaction

## 📧 Email Configuration

Email sending is implemented but requires SMTP credentials.

To enable:

1. Edit `app/services/email_service.py`
2. Uncomment lines 30-33
3. Add your SMTP credentials:

```python
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

For Gmail:
- Enable 2FA
- Generate App Password: https://myaccount.google.com/apppasswords
- Use app password instead of regular password

## 🎯 API Endpoints

### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{id}` - Get product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Denominations
- `POST /api/v1/denominations` - Add denomination
- `GET /api/v1/denominations` - List denominations
- `PUT /api/v1/denominations/{value}` - Update count

### Purchases
- `POST /api/v1/purchases` - Create purchase
- `GET /api/v1/purchases` - List purchases
- `GET /api/v1/purchases/{id}` - Get purchase details

## 🔥 Example Usage

### 1. Add Products via API
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone 15","stock":10,"price":80000,"tax_percent":18}'
```

### 2. Create Purchase via UI
- Open http://127.0.0.1:8000/
- Fill form
- Click "Generate Bill"

### 3. View History
- Click "View Purchase History"
- Click any purchase to see details

## 📊 Database Schema

```
Customer (id, email, created_at)
Product (id, name, stock, price, tax_percent, created_at, updated_at)
Purchase (id, customer_id, total_amount, tax_amount, final_amount, paid_amount, balance_amount, created_at)
PurchaseItem (id, purchase_id, product_id, quantity, unit_price_snapshot, tax_percent_snapshot, tax_amount, total_price)
Denomination (id, value, available_count, updated_at)
PurchaseDenomination (id, purchase_id, denomination_value, count_given)
```

## 🎨 UI Features

- Clean, simple design
- Responsive layout
- Dynamic product rows
- Real-time invoice display
- Purchase history with details
- Error handling with user-friendly messages

## 🔒 Production Considerations

1. **Email**: Configure SMTP credentials
2. **Database**: Use PostgreSQL for production
3. **CORS**: Restrict origins in `main.py`
4. **Security**: Add authentication/authorization
5. **Logging**: Configure proper log levels
6. **Monitoring**: Add health checks and metrics

## 📝 Notes

- Denominations are auto-created with 100 count each
- Email sending is asynchronous (non-blocking)
- Price snapshots ensure historical accuracy
- ACID transactions prevent data corruption
- Stock is automatically updated on purchase

## 🐛 Troubleshooting

**Issue**: Products not found
- **Solution**: Add products via API or Swagger UI first

**Issue**: Email not sending
- **Solution**: Configure SMTP credentials in `email_service.py`

**Issue**: Database error
- **Solution**: Check DATABASE_URL in `.env` file

**Issue**: CORS error
- **Solution**: Check CORS settings in `main.py`

## 📞 Support

For issues or questions, check:
- API Docs: http://127.0.0.1:8000/docs
- Logs: Check console output
- Database: Check `billing.db` file

---

**Built with FastAPI, SQLAlchemy, and vanilla JavaScript**
