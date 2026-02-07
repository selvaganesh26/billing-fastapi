# Billing System API - Production Grade

A production-ready FastAPI billing system with PostgreSQL, implementing clean architecture and ACID transaction management.

## 🏗️ Architecture

```
app/
├── core/           # Configuration, exceptions, utilities
├── db/             # Database configuration
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic schemas for validation
├── crud/           # Repository pattern for data access
├── services/       # Business logic layer
├── routers/        # API endpoints
└── utils/          # Helper functions
```

## 🔥 Key Features

- **ACID Transactions**: Full transaction management for billing operations
- **Price Snapshots**: Historical price preservation (never recompute)
- **Inventory Management**: Automatic stock updates
- **Change Calculation**: Smart denomination breakdown
- **Clean Architecture**: Separation of concerns (Repository → Service → Router)
- **Production Ready**: Connection pooling, logging, error handling

## 📊 Database Schema

### Tables
- **Customer**: Customer information
- **Product**: Product catalog with stock
- **Purchase**: Bill/invoice records
- **PurchaseItem**: Line items with price snapshots
- **Denomination**: Cash denominations available
- **PurchaseDenomination**: Change given tracking

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Edit `.env`:

```env
# For PostgreSQL (Production)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/billing_db

# For SQLite (Development)
DATABASE_URL=sqlite:///./billing.db
```

### 3. Run Application

```bash
uvicorn app.main:app --reload
```

API will be available at: `http://127.0.0.1:8000`

## 📚 API Documentation

Interactive docs: `http://127.0.0.1:8000/docs`

### Endpoints

#### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{id}` - Get product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

#### Denominations
- `POST /api/v1/denominations` - Add denomination
- `GET /api/v1/denominations` - List denominations
- `PUT /api/v1/denominations/{value}` - Update count

#### Purchases (Billing)
- `POST /api/v1/purchases` - Create purchase (Generate Bill)
- `GET /api/v1/purchases` - List purchases
- `GET /api/v1/purchases/{id}` - Get purchase details

## 🔥 Real-World Example

### Step 1: Add Products

```bash
POST /api/v1/products
{
  "name": "iPhone 15",
  "stock": 10,
  "price": 80000,
  "tax_percent": 18
}
```

### Step 2: Add Denominations

```bash
POST /api/v1/denominations
{
  "value": 500,
  "available_count": 100
}
```

### Step 3: Create Purchase (Generate Bill)

```bash
POST /api/v1/purchases
{
  "customer_email": "selva@gmail.com",
  "items": [
    {"product_id": 1, "quantity": 1},
    {"product_id": 2, "quantity": 2}
  ],
  "paid_amount": 120000
}
```

### What Happens Behind the Scenes:

1. ✅ Customer created/fetched
2. ✅ Products validated (stock check)
3. ✅ Totals calculated (with tax)
4. ✅ Purchase record created
5. ✅ Purchase items created (with price snapshots)
6. ✅ Inventory updated (stock reduced)
7. ✅ Change calculated and denominations updated
8. ✅ Transaction committed

**If ANY step fails → ROLLBACK (ACID guarantee)**

## 🎯 Production Best Practices

### 1. Transaction Management
All billing operations wrapped in database transactions with proper rollback.

### 2. Price Snapshots
Product prices frozen at purchase time - historical data never changes.

### 3. Stock Management
Automatic inventory updates with constraint checks.

### 4. Error Handling
Custom exceptions with proper HTTP status codes.

### 5. Repository Pattern
Clean separation between data access and business logic.

### 6. Connection Pooling
Configured for production with pool size and overflow limits.

### 7. Logging
Comprehensive logging for debugging and monitoring.

## 🔒 Database Constraints

- Stock cannot be negative
- Price must be positive
- Tax percent must be non-negative
- Denomination counts must be non-negative
- Foreign key constraints enforced

## 📈 Scaling Considerations

1. **Database**: Use PostgreSQL with proper indexing
2. **Caching**: Add Redis for frequently accessed data
3. **Queue**: Use Celery for async operations (emails, reports)
4. **Monitoring**: Add Prometheus + Grafana
5. **Load Balancing**: Deploy behind Nginx/Traefik

## 🧪 Testing

```bash
# Run tests (add pytest)
pytest tests/

# Check coverage
pytest --cov=app tests/
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./billing.db |
| PROJECT_NAME | API project name | Billing System API |
| VERSION | API version | 1.0.0 |
| API_V1_PREFIX | API prefix | /api/v1 |

## 🤝 Contributing

This is a production-grade template. Customize based on your requirements.

## 📄 License

MIT License
