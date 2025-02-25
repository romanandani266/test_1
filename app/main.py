from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
mock_inventory = []
mock_alerts = []
mock_sales = []
mock_users = [{"username": "admin", "password": "admin", "role": "admin"}]

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    id: int
    product_name: str
    category: Optional[str]
    quantity: int
    last_updated: datetime

class Alert(BaseModel):
    id: int
    product_id: int
    threshold: int
    created_at: datetime

class SalesTrend(BaseModel):
    product_id: int
    sales_data: List[dict]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/api/auth/login", response_model=Token)
def login(user: User):
    for mock_user in mock_users:
        if user.username == mock_user["username"] and user.password == mock_user["password"]:
            access_token = create_access_token(data={"sub": user.username, "role": mock_user["role"]})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(product_id: Optional[int] = None, category: Optional[str] = None):
    filtered_inventory = mock_inventory
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item.id == product_id]
    if category:
        filtered_inventory = [item for item in filtered_inventory if item.category == category]
    return filtered_inventory

@app.post("/api/inventory", response_model=dict)
def add_inventory(item: InventoryItem):
    mock_inventory.append(item)
    return {"message": "Inventory item added successfully", "id": item.id}

@app.put("/api/inventory/{id}", response_model=dict)
def update_inventory(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory[i] = item
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")

@app.delete("/api/inventory/{id}", response_model=dict)
def delete_inventory(id: int):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory.pop(i)
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts(product_id: Optional[int] = None):
    filtered_alerts = mock_alerts
    if product_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert.product_id == product_id]
    return filtered_alerts

@app.post("/api/alerts", response_model=dict)
def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return {"message": "Alert created successfully", "id": alert.id}

@app.delete("/api/alerts/{id}", response_model=dict)
def delete_alert(id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.id == id:
            mock_alerts.pop(i)
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

@app.get("/api/sales/trends", response_model=SalesTrend)
def get_sales_trends(product_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    sales_data = [{"date": "2023-01-01", "quantity_sold": 10}, {"date": "2023-01-02", "quantity_sold": 15}]
    if start_date or end_date:
        sales_data = [data for data in sales_data if (not start_date or data["date"] >= start_date) and (not end_date or data["date"] <= end_date)]
    return {"product_id": product_id, "sales_data": sales_data}