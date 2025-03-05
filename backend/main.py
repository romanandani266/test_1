from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

users = [{"user_id": 1, "username": "admin", "password_hash": "admin123", "role": "admin"}]
inventory = []
alerts = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
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

@app.post("/api/auth/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and u["password_hash"] == user.password:
            return {"token": "fake-jwt-token", "role": u["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logged out successfully"}

@app.get("/api/inventory")
def get_inventory():
    return inventory

@app.post("/api/inventory")
def add_inventory_item(item: InventoryItem):
    inventory.append(item.dict())
    return {"message": "Inventory item added successfully"}

@app.put("/api/inventory/{id}")
def update_inventory_item(id: int, item: InventoryItem):
    for i, inv_item in enumerate(inventory):
        if inv_item["product_id"] == id:
            inventory[i] = item.dict()
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    for i, inv_item in enumerate(inventory):
        if inv_item["product_id"] == id:
            inventory.pop(i)
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts")
def get_alerts():
    return alerts

@app.post("/api/alerts")
def create_alert(alert: Alert):
    alerts.append(alert.dict())
    return {"message": "Alert created successfully"}

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    for i, alert in enumerate(alerts):
        if alert["alert_id"] == id:
            alerts.pop(i)
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends")
def get_sales_trends():
    sales_trends = [
        {"product_id": 1, "sales_data": [10, 20, 15]},
        {"product_id": 2, "sales_data": [5, 8, 12]},
    ]
    return sales_trends