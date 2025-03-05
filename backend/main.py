from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

users = [{"user_id": "1", "username": "admin", "password": "admin", "role": "admin"}]
inventory = []
alerts = []

class User(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: str
    product_id: str
    product_name: str
    category: str
    price: float
    quantity: int

class Alert(BaseModel):
    alert_id: str
    product_id: str
    threshold: int
    status: str

class SalesTrendReport(BaseModel):
    product_id: str
    product_name: str
    sales_trend: str

@app.post("/api/auth/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            return {"token": str(uuid4()), "role": u["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory_item(item: InventoryItem):
    inventory.append(item)
    return item

@app.put("/api/inventory/{id}", response_model=InventoryItem)
def update_inventory_item(id: str, updated_item: InventoryItem):
    for item in inventory:
        if item.inventory_id == id:
            item.product_id = updated_item.product_id
            item.product_name = updated_item.product_name
            item.category = updated_item.category
            item.price = updated_item.price
            item.quantity = updated_item.quantity
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: str):
    global inventory
    inventory = [item for item in inventory if item.inventory_id != id]
    return {"message": "Item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    alerts.append(alert)
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: str):
    global alerts
    alerts = [alert for alert in alerts if alert.alert_id != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
def get_sales_trends():
    sales_trends = [
        {"product_id": "101", "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": "102", "product_name": "Product B", "sales_trend": "Decreasing"},
    ]
    return sales_trends
