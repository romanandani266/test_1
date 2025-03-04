from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

users = [{"user_id": 1, "username": "admin", "password": "admin123", "role": "admin"}]
inventory = []
alerts = []

class UserLogin(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: int
    product_id: int
    quantity: int

class NewInventoryItem(BaseModel):
    product_id: int
    quantity: int

class UpdateInventoryItem(BaseModel):
    product_id: Optional[int]
    quantity: Optional[int]

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int
    status: str

class NewAlert(BaseModel):
    product_id: int
    threshold: int
    status: str

class SalesTrendReport(BaseModel):
    product_id: int
    product_name: str
    sales_trend: str

def authenticate_user(username: str, password: str):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        for user in users:
            if user["username"] == username:
                return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/login")
def login(user: UserLogin):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": authenticated_user["username"]})
    return {"access_token": access_token, "token_type": "bearer", "role": authenticated_user["role"]}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return inventory

@app.post("/api/inventory")
def add_inventory_item(item: NewInventoryItem):
    new_item = {
        "inventory_id": len(inventory) + 1,
        "product_id": item.product_id,
        "quantity": item.quantity
    }
    inventory.append(new_item)
    return {"message": "Inventory item added successfully", "item": new_item}

@app.put("/api/inventory/{id}")
def update_inventory_item(id: int, item: UpdateInventoryItem):
    for inv_item in inventory:
        if inv_item["inventory_id"] == id:
            if item.product_id is not None:
                inv_item["product_id"] = item.product_id
            if item.quantity is not None:
                inv_item["quantity"] = item.quantity
            return {"message": "Inventory item updated successfully", "item": inv_item}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    global inventory
    inventory = [item for item in inventory if item["inventory_id"] != id]
    return {"message": "Inventory item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return alerts

@app.post("/api/alerts")
def create_alert(alert: NewAlert):
    new_alert = {
        "alert_id": len(alerts) + 1,
        "product_id": alert.product_id,
        "threshold": alert.threshold,
        "status": alert.status
    }
    alerts.append(new_alert)
    return {"message": "Alert created successfully", "alert": new_alert}

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    global alerts
    alerts = [alert for alert in alerts if alert["alert_id"] != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
def get_sales_trends():
    sales_trends = [
        {"product_id": 1, "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": 2, "product_name": "Product B", "sales_trend": "Stable"},
    ]
    return sales_trends