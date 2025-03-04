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

mock_inventory = []
mock_alerts = []
mock_users = [{"username": "admin", "password": "admin123", "role": "admin"}]

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class InventoryItem(BaseModel):
    id: int
    product_name: str
    category: str
    price: float
    quantity: int

class Alert(BaseModel):
    id: int
    product_id: int
    threshold: int
    status: str

def authenticate_user(username: str, password: str):
    for user in mock_users:
        if user["username"] == username and user["password"] == password:
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
def login(user: User):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user["username"], "role": authenticated_user["role"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer", "role": authenticated_user["role"]}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return mock_inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory_item(item: InventoryItem):
    mock_inventory.append(item)
    return item

@app.put("/api/inventory/{id}", response_model=InventoryItem)
def update_inventory_item(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            del mock_inventory[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.id == id:
            del mock_alerts[i]
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends")
def get_sales_trends():
    return {"message": "Sales trend analysis not implemented yet"}