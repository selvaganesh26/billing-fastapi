from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import product
from app.routers import product_router

app = FastAPI(title="Billing FastAPI")
# Create tables automatically (good for beginners)
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Billing API is running 🚀"}

app.include_router(product_router.router)
