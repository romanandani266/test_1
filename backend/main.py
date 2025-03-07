from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

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

users = [
    {"user_id": str(uuid4()), "username": "admin", "password": "admin123", "role": "admin"},
    {"user_id": str(uuid4()), "username": "manager", "password": "manager123", "role": "manager"},
]

products = []
alerts = []
sales_trends = []

class UserLogin(BaseModel):
    username: str
    password: str

class Product(BaseModel):
    product_id: Optional[str]
    product_name: str
    quantity: int
    threshold: int

class Alert(BaseModel):
    alert_id: Optional[str]
    product_id: str
    alert_message: str

class SalesTrend(BaseModel):
    trend_id: Optional[str]
    product_id: str
    sales_date: str
    quantity_sold: int

@app.post("/api/auth/login")
async def login(user: UserLogin):
    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            return {"access_token": u["username"], "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/api/auth/logout")
async def logout():
    return {"message": "User logged out successfully"}

@app.get("/api/inventory", response_model=List[Product])
async def get_inventory():
    return products

@app.post("/api/inventory", response_model=Product)
async def add_new_product(product: Product):
    product.product_id = str(uuid4())
    products.append(product.dict())
    return product

@app.put("/api/inventory", response_model=Product)
async def update_inventory(product: Product):
    for p in products:
        if p["product_id"] == product.product_id:
            p["quantity"] = product.quantity
            if p["quantity"] < p["threshold"]:
                alert = Alert(
                    alert_id=str(uuid4()),
                    product_id=p["product_id"],
                    alert_message=f"Stock for {p['product_name']} is below threshold!"
                )
                alerts.append(alert.dict())
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/api/inventory/{product_id}")
async def delete_product(product_id: str):
    global products
    products = [p for p in products if p["product_id"] != product_id]
    return {"message": "Product deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    return alerts

@app.delete("/api/alerts/{alert_id}")
async def dismiss_alert(alert_id: str):
    global alerts
    alerts = [a for a in alerts if a["alert_id"] != alert_id]
    return {"message": "Alert dismissed successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrend])
async def get_sales_trends():
    return sales_trends
