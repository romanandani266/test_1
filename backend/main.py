from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"},
}

class LoginRequest(BaseModel):
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

class SalesTrendReport(BaseModel):
    product_id: int
    product_name: str
    sales_trend: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in mock_users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return mock_users[token]

def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@app.post("/api/auth/login")
def login(request: LoginRequest):
    for user, details in mock_users.items():
        if request.username == details["username"] and request.password == details["password"]:
            return {"token": user, "role": details["role"]}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    if token not in mock_users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return [
        {"inventory_id": 1, "product_id": 1, "product_name": "Product A", "category": "Category 1", "price": 10.0, "quantity": 100},
        {"inventory_id": 2, "product_id": 2, "product_name": "Product B", "category": "Category 2", "price": 20.0, "quantity": 50},
    ]

@app.post("/api/inventory")
def add_inventory(item: InventoryItem, current_user: dict = Depends(get_admin_user)):
    return {"message": "Inventory item added successfully", "item": item}

@app.put("/api/inventory/{id}")
def update_inventory(id: int, item: InventoryItem, current_user: dict = Depends(get_admin_user)):
    return {"message": f"Inventory item {id} updated successfully", "item": item}

@app.delete("/api/inventory/{id}")
def delete_inventory(id: int, current_user: dict = Depends(get_admin_user)):
    return {"message": f"Inventory item {id} deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return [
        {"alert_id": 1, "product_id": 1, "threshold": 20, "status": "active"},
        {"alert_id": 2, "product_id": 2, "threshold": 10, "status": "inactive"},
    ]

@app.post("/api/alerts")
def create_alert(alert: Alert, current_user: dict = Depends(get_admin_user)):
    return {"message": "Alert created successfully", "alert": alert}

@app.delete("/api/alerts/{id}")
def delete_alert(id: int, current_user: dict = Depends(get_admin_user)):
    return {"message": f"Alert {id} deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
def get_sales_trends():
    return [
        {"product_id": 1, "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": 2, "product_name": "Product B", "sales_trend": "Decreasing"},
    ]