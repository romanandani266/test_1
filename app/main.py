from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

mock_inventory = []
mock_alerts = []
mock_sales = []
mock_users = [{"username": "admin", "password": "admin123", "role": "admin"}]

class UserLogin(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    product_id: int
    product_name: str
    category: Optional[str]
    quantity: int
    price: float

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int

class SalesTrend(BaseModel):
    product_id: int
    quantity_sold: int
    sale_date: datetime

@app.post("/api/auth/login")
async def login(user: UserLogin):
    for mock_user in mock_users:
        if user.username == mock_user["username"] and user.password == mock_user["password"]:
            return {"access_token": "mock_jwt_token", "token_type": "bearer", "role": mock_user["role"]}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Successfully logged out"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory(product_id: Optional[int] = None, category: Optional[str] = None):
    filtered_inventory = mock_inventory
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item.product_id == product_id]
    if category:
        filtered_inventory = [item for item in filtered_inventory if item.category == category]
    return filtered_inventory

@app.post("/api/inventory")
async def add_inventory(item: InventoryItem):
    mock_inventory.append(item)
    return {"message": "Inventory item added successfully", "item_id": len(mock_inventory)}

@app.put("/api/inventory/{id}")
async def update_inventory(id: int, item: InventoryItem):
    for i, inventory_item in enumerate(mock_inventory):
        if inventory_item.product_id == id:
            mock_inventory[i] = item
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
async def delete_inventory(id: int):
    for i, inventory_item in enumerate(mock_inventory):
        if inventory_item.product_id == id:
            del mock_inventory[i]
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts(product_id: Optional[int] = None):
    filtered_alerts = mock_alerts
    if product_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert.product_id == product_id]
    return filtered_alerts

@app.post("/api/alerts")
async def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return {"message": "Alert created successfully", "alert_id": len(mock_alerts)}

@app.delete("/api/alerts/{id}")
async def delete_alert(id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.alert_id == id:
            del mock_alerts[i]
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends", response_model=List[SalesTrend])
async def get_sales_trends(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, product_id: Optional[int] = None):
    filtered_sales = mock_sales
    if start_date:
        filtered_sales = [sale for sale in filtered_sales if sale.sale_date >= start_date]
    if end_date:
        filtered_sales = [sale for sale in filtered_sales if sale.sale_date <= end_date]
    if product_id:
        filtered_sales = [sale for sale in filtered_sales if sale.product_id == product_id]
    return filtered_sales

@app.get("/")
async def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}