from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

app = FastAPI()

users = [{"user_id": 1, "username": "admin", "password": "admin123", "role": "admin"}]
inventory = []
alerts = []

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class User(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    inventory_id: int
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

class SalesTrend(BaseModel):
    product_id: int
    product_name: str
    sales_data: List[int]

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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
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
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logout successful"}

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
        if inv_item["inventory_id"] == id:
            inventory[i] = item.dict()
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    for i, inv_item in enumerate(inventory):
        if inv_item["inventory_id"] == id:
            inventory.pop(i)
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

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
        {"product_id": 1, "product_name": "Product A", "sales_data": [100, 120, 90]},
        {"product_id": 2, "product_name": "Product B", "sales_data": [80, 95, 110]},
    ]
    return sales_trends