from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": "user123",
        "role": "user"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    role: str

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
    sales_data: List[dict]

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(username=username, role=user["role"])

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    inventory = [
        {"id": 1, "product_id": 101, "quantity": 50, "last_updated": datetime.now()},
        {"id": 2, "product_id": 102, "quantity": 30, "last_updated": datetime.now()},
    ]
    return inventory

@app.post("/api/inventory")
def add_inventory(item: InventoryItem):
    return {"message": "Inventory item added successfully", "item_id": item.id}

@app.put("/api/inventory/{id}")
def update_inventory(id: int, item: InventoryItem):
    return {"message": f"Inventory item {id} updated successfully"}

@app.delete("/api/inventory/{id}")
def delete_inventory(id: int):
    return {"message": f"Inventory item {id} deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    alerts = [
        {"id": 1, "product_id": 101, "threshold": 10, "created_at": datetime.now()},
        {"id": 2, "product_id": 102, "threshold": 5, "created_at": datetime.now()},
    ]
    return alerts

@app.post("/api/alerts")
def create_alert(alert: Alert):
    return {"message": "Alert created successfully", "alert_id": alert.id}

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    return {"message": f"Alert {id} deleted successfully"}

@app.get("/api/sales/trends", response_model=SalesTrend)
def get_sales_trends():
    trends = {
        "product_id": 101,
        "sales_data": [
            {"date": "2023-01-01", "quantity_sold": 10},
            {"date": "2023-01-02", "quantity_sold": 15},
        ],
    }
    return trends