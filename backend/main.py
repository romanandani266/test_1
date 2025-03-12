from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    viewer = "viewer"

class Product(BaseModel):
    id: int
    name: str
    category: str
    stock_level: int
    restock_threshold: int
    sales_trend: Optional[List[int]] = None

class User(BaseModel):
    username: str
    password: str
    role: Role

products = [
    Product(id=1, name="Pepsi", category="Beverages", stock_level=50, restock_threshold=20, sales_trend=[100, 120, 90]),
    Product(id=2, name="Lays", category="Snacks", stock_level=30, restock_threshold=10, sales_trend=[80, 70, 60]),
]

users = [
    User(username="admin_user", password="admin123", role=Role.admin),
    User(username="manager_user", password="manager123", role=Role.manager),
    User(username="viewer_user", password="viewer123", role=Role.viewer),
]

def get_current_user(role: Role):
    def dependency(username: str):
        user = next((u for u in users if u.username == username), None)
        if not user or user.role != role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return dependency

@app.get("/")
def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}

@app.get("/products", response_model=List[Product])
def get_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, dependencies=[Depends(get_current_user(Role.admin))])
def add_product(product: Product):
    if any(p.id == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(product)
    return product

@app.put("/products/{product_id}", response_model=Product, dependencies=[Depends(get_current_user(Role.manager))])
def update_product(product_id: int, updated_product: Product):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = updated_product.name
    product.category = updated_product.category
    product.stock_level = updated_product.stock_level
    product.restock_threshold = updated_product.restock_threshold
    product.sales_trend = updated_product.sales_trend
    return product

@app.delete("/products/{product_id}", dependencies=[Depends(get_current_user(Role.admin))])
def delete_product(product_id: int):
    global products
    products = [p for p in products if p.id != product_id]
    return {"message": "Product deleted successfully"}

@app.get("/alerts", response_model=List[str])
def get_restock_alerts():
    alerts = []
    for product in products:
        if product.stock_level <= product.restock_threshold:
            alerts.append(f"Product '{product.name}' needs restocking. Current stock: {product.stock_level}")
    return alerts

@app.get("/sales-trends/{product_id}", response_model=List[int])
def get_sales_trend(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.sales_trend

@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    user = next((u for u in users if u.username == username and u.password == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": f"Welcome {user.username}", "role": user.role}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}