from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

mock_inventory = []
mock_alerts = []
mock_users = [{"user_id": 1, "username": "admin", "password_hash": "admin123", "role": "admin"}]

class User(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: int
    product_id: int
    product_name: str
    category: str
    price: float
    quantity: int

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int
    status: str

class SalesTrendReport(BaseModel):
    product_id: int
    product_name: str
    sales_trend: str

@app.post("/api/auth/login")
async def login(user: User):
    for mock_user in mock_users:
        if user.username == mock_user["username"] and user.password == mock_user["password_hash"]:
            return {"token": "mock-jwt-token", "role": mock_user["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory():
    return mock_inventory

@app.post("/api/inventory", response_model=InventoryItem)
async def add_inventory_item(item: InventoryItem):
    mock_inventory.append(item)
    return item

@app.put("/api/inventory/{inventory_id}", response_model=InventoryItem)
async def update_inventory_item(inventory_id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.inventory_id == inventory_id:
            mock_inventory[i] = item
            return item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{inventory_id}")
async def delete_inventory_item(inventory_id: int):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.inventory_id == inventory_id:
            del mock_inventory[i]
            return {"message": "Inventory item deleted"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
async def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return alert

@app.delete("/api/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.alert_id == alert_id:
            del mock_alerts[i]
            return {"message": "Alert deleted"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
async def get_sales_trends():
    mock_sales_trends = [
        {"product_id": 1, "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": 2, "product_name": "Product B", "sales_trend": "Stable"},
    ]
    return mock_sales_trends