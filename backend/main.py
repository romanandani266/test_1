from fastapi import FastAPI, HTTPException
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

mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"},
}

mock_inventory = [
    {"inventory_id": 1, "product_id": 101, "product_name": "Pepsi", "quantity": 50},
    {"inventory_id": 2, "product_id": 102, "product_name": "Lays", "quantity": 30},
]

mock_alerts = [
    {"alert_id": 1, "product_id": 101, "threshold": 20, "status": "active"},
]

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: int
    product_id: int
    product_name: str
    quantity: int

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int
    status: str

class SalesTrend(BaseModel):
    product_id: int
    product_name: str
    sales_data: List[int]

def authenticate_user(username: str, password: str):
    user = mock_users.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/auth/login", response_model=Token)
def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return mock_inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory(item: InventoryItem):
    mock_inventory.append(item.dict())
    return item

@app.put("/api/inventory/{id}", response_model=InventoryItem)
def update_inventory(id: int, item: InventoryItem):
    for inv in mock_inventory:
        if inv["inventory_id"] == id:
            inv.update(item.dict())
            return item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory(id: int):
    global mock_inventory
    mock_inventory = [inv for inv in mock_inventory if inv["inventory_id"] != id]
    return {"message": "Inventory item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    mock_alerts.append(alert.dict())
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    global mock_alerts
    mock_alerts = [alert for alert in mock_alerts if alert["alert_id"] != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrend])
def get_sales_trends():
    sales_trends = [
        {"product_id": 101, "product_name": "Pepsi", "sales_data": [100, 120, 90]},
        {"product_id": 102, "product_name": "Lays", "sales_data": [80, 95, 110]},
    ]
    return sales_trends