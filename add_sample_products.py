"""
Script to add sample products to the billing system
Run this after starting the server
"""
import requests

API_BASE = "http://127.0.0.1:8000/api/v1"

# Sample products
products = [
    {"name": "iPhone 15", "stock": 10, "price": 80000, "tax_percent": 18},
    {"name": "AirPods Pro", "stock": 20, "price": 15000, "tax_percent": 12},
    {"name": "MacBook Pro", "stock": 5, "price": 150000, "tax_percent": 18},
    {"name": "iPad Air", "stock": 15, "price": 60000, "tax_percent": 18},
    {"name": "Apple Watch", "stock": 25, "price": 45000, "tax_percent": 12},
]

print("Adding sample products...")
print("-" * 50)

for product in products:
    try:
        response = requests.post(f"{API_BASE}/products", json=product)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Created: {data['name']} (ID: {data['id']})")
        else:
            print(f"✗ Failed: {product['name']} - {response.json()}")
    except Exception as e:
        print(f"✗ Error: {product['name']} - {str(e)}")

print("-" * 50)
print("Done! Products added successfully.")
print("\nYou can now:")
print("1. Visit http://127.0.0.1:8000/ to create bills")
print("2. Visit http://127.0.0.1:8000/docs to see API documentation")
