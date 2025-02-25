from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

mock_inventory = []
mock_alerts = []
mock_sales = []

class UserLogin(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: int
    product_id: int
    product_name: str
    category: Optional[str]
    quantity: int
    last_updated: Optional[datetime] = datetime.now()

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int
    created_at: Optional[datetime] = datetime.now()

class SalesTrend(BaseModel):
    product_id: int
    product_name: str
    total_sales: int
    trend: str

@app.post("/api/auth/login")
async def login(user: UserLogin):
    if user.username == "admin" and user.password == "password":
        return {"token": "mock-jwt-token", "role": "admin"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory(product_id: Optional[int] = Query(None), category: Optional[str] = Query(None)):
    if product_id:
        return [item for item in mock_inventory if item.product_id == product_id]
    if category:
        return [item for item in mock_inventory if item.category == category]
    return mock_inventory

@app.post("/api/inventory")
async def add_inventory(item: InventoryItem):
    mock_inventory.append(item)
    return {"message": "Inventory item added successfully", "inventory_id": len(mock_inventory)}

@app.put("/api/inventory/{id}")
async def update_inventory(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.inventory_id == id:
            mock_inventory[i] = item
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
async def delete_inventory(id: int):
    global mock_inventory
    mock_inventory = [item for item in mock_inventory if item.inventory_id != id]
    return {"message": "Inventory item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    return mock_alerts

@app.post("/api/alerts")
async def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return {"message": "Alert created successfully", "alert_id": len(mock_alerts)}

@app.delete("/api/alerts/{id}")
async def delete_alert(id: int):
    global mock_alerts
    mock_alerts = [alert for alert in mock_alerts if alert.alert_id != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrend])
async def get_sales_trends(start_date: Optional[str] = Query(None), end_date: Optional[str] = Query(None)):
    return [
        SalesTrend(product_id=1, product_name="Product A", total_sales=100, trend="upward"),
        SalesTrend(product_id=2, product_name="Product B", total_sales=50, trend="downward"),
    ]

@app.get("/")
async def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}