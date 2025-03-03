from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"},
}

mock_inventory = [
    {"inventory_id": 1, "product_id": 101, "quantity": 50},
    {"inventory_id": 2, "product_id": 102, "quantity": 20},
]

mock_alerts = [
    {"alert_id": 1, "product_id": 101, "threshold": 10, "status": "active"},
]

mock_sales_trends = [
    {"product_id": 101, "trend": "increasing"},
    {"product_id": 102, "trend": "stable"},
]

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class InventoryItem(BaseModel):
    inventory_id: int
    product_id: int
    quantity: int

class Alert(BaseModel):
    alert_id: int
    product_id: int
    threshold: int
    status: str

class SalesTrend(BaseModel):
    product_id: int
    trend: str

def authenticate_user(username: str, password: str):
    user = mock_users.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return mock_users.get(username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

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
            return inv
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
    return mock_sales_trends