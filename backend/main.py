from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import timedelta, datetime
from jose import jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

mock_inventory = []
mock_alerts = []
mock_users = [{"username": "admin", "password": "admin123", "role": "admin"}]

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

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

class SalesTrendReport(BaseModel):
    product_id: int
    product_name: str
    sales_trend: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in mock_users if u["username"] == form_data.username and u["password"] == form_data.password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
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
    global mock_inventory
    mock_inventory = [item for item in mock_inventory if item.id != id]
    return {"message": "Item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    global mock_alerts
    mock_alerts = [alert for alert in mock_alerts if alert.id != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
def get_sales_trends():
    mock_sales_trends = [
        {"product_id": 1, "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": 2, "product_name": "Product B", "sales_trend": "Stable"},
    ]
    return mock_sales_trends