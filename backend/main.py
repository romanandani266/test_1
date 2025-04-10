from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

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

mock_inventory = [
    {"location_id": "loc1", "product_id": "prod1", "stock_level": 50, "threshold": 20},
    {"location_id": "loc2", "product_id": "prod2", "stock_level": 10, "threshold": 15},
]

mock_sales = [
    {"product_id": "prod1", "location_id": "loc1", "quantity_sold": 100, "sale_date": "2023-10-01"},
    {"product_id": "prod2", "location_id": "loc2", "quantity_sold": 50, "sale_date": "2023-10-02"},
]

mock_alerts = [
    {"alert_id": str(uuid4()), "product_id": "prod2", "location_id": "loc2", "alert_date": "2023-10-03", "status": "pending"},
]

mock_users = [
    {"user_id": str(uuid4()), "username": "admin", "password": "admin123", "role": "admin"},
    {"user_id": str(uuid4()), "username": "manager", "password": "manager123", "role": "manager"},
]

class Inventory(BaseModel):
    location_id: str
    product_id: str
    stock_level: int
    threshold: int

class InventoryUpdate(BaseModel):
    location_id: str
    product_id: str
    new_stock_level: int

class RestockingAlert(BaseModel):
    product_id: str
    location_id: str
    contact_details: str

class SalesTrend(BaseModel):
    product_id: Optional[str]
    date_range: Optional[str]

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/api/auth/login")
def login(user: UserLogin):
    for mock_user in mock_users:
        if mock_user["username"] == user.username and mock_user["password"] == user.password:
            return {"message": "Login successful", "user_id": mock_user["user_id"], "role": mock_user["role"]}
    raise HTTPException(status_code=401, detail="Invalid username or password.")

@app.get("/api/inventory", response_model=List[Inventory])
def get_inventory(location_id: Optional[str] = None, product_id: Optional[str] = None):
    filtered_inventory = mock_inventory
    if location_id:
        filtered_inventory = [item for item in filtered_inventory if item["location_id"] == location_id]
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item["product_id"] == product_id]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found.")
    return filtered_inventory

@app.post("/api/inventory/update")
def update_inventory(update: InventoryUpdate):
    for item in mock_inventory:
        if item["location_id"] == update.location_id and item["product_id"] == update.product_id:
            item["stock_level"] = update.new_stock_level
            return {"message": "Inventory updated successfully.", "updated_inventory": item}
    raise HTTPException(status_code=404, detail="Inventory record not found.")

@app.get("/api/alerts/restocking")
def get_restocking_alerts(location_id: Optional[str] = None):
    alerts = [
        {"product_id": item["product_id"], "location_id": item["location_id"]}
        for item in mock_inventory if item["stock_level"] < item["threshold"]
    ]
    if location_id:
        alerts = [alert for alert in alerts if alert["location_id"] == location_id]
    if not alerts:
        raise HTTPException(status_code=404, detail="No restocking alerts found.")
    return alerts

@app.post("/api/alerts/notify")
def send_restocking_notification(alert: RestockingAlert):
    return {"message": "Restocking notification sent successfully.", "alert_details": alert}

@app.get("/api/sales/trends")
def get_sales_trends(product_id: Optional[str] = None, date_range: Optional[str] = None):
    filtered_sales = mock_sales
    if product_id:
        filtered_sales = [sale for sale in filtered_sales if sale["product_id"] == product_id]
    if not filtered_sales:
        raise HTTPException(status_code=404, detail="No sales data found.")
    return filtered_sales

@app.get("/")
def root():
    return {"message": "Welcome to the Retail Inventory Management System API!"}