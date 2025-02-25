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
    id: Optional[int]
    product_id: int
    quantity: int
    last_updated: Optional[datetime] = datetime.now()

class Alert(BaseModel):
    id: Optional[int]
    product_id: int
    threshold: int
    created_at: Optional[datetime] = datetime.now()

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/api/auth/login", response_model=Token)
def login(user: User):
    for mock_user in mock_users:
        if user.username == mock_user["username"] and user.password == mock_user["password"]:
            access_token = create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return mock_inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory(item: InventoryItem):
    item.id = len(mock_inventory) + 1
    mock_inventory.append(item)
    return item

@app.put("/api/inventory/{id}")
def update_inventory(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory[i] = item
            return {"message": "Inventory updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory(id: int):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            del mock_inventory[i]
            return {"message": "Inventory deleted successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    alert.id = len(mock_alerts) + 1
    mock_alerts.append(alert)
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.id == id:
            del mock_alerts[i]
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends", response_model=List[SalesTrend])
def get_sales_trends():
    return mock_sales