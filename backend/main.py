from fastapi import FastAPI, HTTPException, Depends
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

mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "manager": {"username": "manager", "password": "manager123", "role": "manager"},
}

mock_inventory = {}
mock_notifications = []
mock_sales = []

class LoginRequest(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    product_id: str
    product_name: str
    stock_level: int
    threshold: int

class Notification(BaseModel):
    notification_id: str
    product_id: str
    message: str
    is_read: bool

class SalesData(BaseModel):
    sale_id: str
    product_id: str
    quantity_sold: int
    sale_date: str
    total_revenue: float

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    user = mock_users.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": str(uuid4()), "user_role": user["role"]}

@app.post("/api/auth/logout")
async def logout():
    return {"message": "User logged out successfully"}

@app.get("/api/inventory")
async def get_inventory(product_id: Optional[str] = None):
    if product_id:
        item = mock_inventory.get(product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        return item
    return list(mock_inventory.values())

@app.post("/api/inventory")
async def add_inventory(item: InventoryItem):
    if item.product_id in mock_inventory:
        raise HTTPException(status_code=400, detail="Product already exists")
    mock_inventory[item.product_id] = item.dict()
    return {"message": "Product added successfully"}

@app.put("/api/inventory/{product_id}")
async def update_inventory(product_id: str, stock_level: Optional[int] = None, threshold: Optional[int] = None):
    item = mock_inventory.get(product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    if stock_level is not None:
        item["stock_level"] = stock_level
    if threshold is not None:
        item["threshold"] = threshold
    mock_inventory[product_id] = item
    return {"message": "Product updated successfully"}

@app.delete("/api/inventory/{product_id}")
async def delete_inventory(product_id: str):
    if product_id not in mock_inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    del mock_inventory[product_id]
    return {"message": "Product deleted successfully"}

@app.get("/api/notifications")
async def get_notifications():
    return mock_notifications

@app.get("/api/sales")
async def get_sales(start_date: Optional[str] = None, end_date: Optional[str] = None):
    if start_date and end_date:
        filtered_sales = [
            sale for sale in mock_sales
            if start_date <= sale["sale_date"] <= end_date
        ]
        return filtered_sales
    return mock_sales

@app.middleware("http")
async def stock_alert_middleware(request, call_next):
    response = await call_next(request)
    for product_id, item in mock_inventory.items():
        if item["stock_level"] < item["threshold"]:
            notification = {
                "notification_id": str(uuid4()),
                "product_id": product_id,
                "message": f"Stock level for {item['product_name']} is below threshold!",
                "is_read": False,
            }
            mock_notifications.append(notification)
    return response