from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

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

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users = {"admin": {"username": "admin", "password": "admin", "role": "admin"}}
inventory = []
alerts = []
sales = []

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    last_updated: datetime

class Alert(BaseModel):
    id: int
    product_id: int
    threshold: int
    created_at: datetime

class SalesTrend(BaseModel):
    product_id: int
    quantity_sold: int
    sale_date: datetime

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/auth/login", response_model=Token)
def login(user: UserLogin):
    stored_user = users.get(user.username)
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory_item(item: InventoryItem):
    inventory.append(item)
    return item

@app.put("/api/inventory/{id}")
def update_inventory_item(id: int, updated_item: InventoryItem):
    for item in inventory:
        if item.id == id:
            item.product_id = updated_item.product_id
            item.quantity = updated_item.quantity
            item.last_updated = datetime.utcnow()
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    global inventory
    inventory = [item for item in inventory if item.id != id]
    return {"message": "Inventory item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    alerts.append(alert)
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    global alerts
    alerts = [alert for alert in alerts if alert.id != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrend])
def get_sales_trends():
    return sales