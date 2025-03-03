from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional

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
    id: Optional[int]
    product_name: str
    category: str
    price: float
    quantity: int

class Alert(BaseModel):
    id: Optional[int]
    product_id: int
    threshold: int
    status: str

class SalesTrendReport(BaseModel):
    product_id: int
    product_name: str
    sales_trend: str

mock_inventory = [
    {"id": 1, "product_name": "Pepsi", "category": "Beverage", "price": 1.5, "quantity": 100},
    {"id": 2, "product_name": "Lays", "category": "Snacks", "price": 2.0, "quantity": 50},
]
mock_alerts = [
    {"id": 1, "product_id": 1, "threshold": 20, "status": "active"},
]
mock_sales_trends = [
    {"product_id": 1, "product_name": "Pepsi", "sales_trend": "increasing"},
    {"product_id": 2, "product_name": "Lays", "sales_trend": "stable"},
]

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = mock_users.get(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

@app.post("/api/auth/login")
def login(request: LoginRequest):
    for user in mock_users.values():
        if user["username"] == request.username and user["password"] == request.password:
            return {"token": request.username, "role": user["role"]}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logged out successfully"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return mock_inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory_item(item: InventoryItem):
    item.id = len(mock_inventory) + 1
    mock_inventory.append(item.dict())
    return item

@app.put("/api/inventory/{id}", response_model=InventoryItem)
def update_inventory_item(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item["id"] == id:
            mock_inventory[i] = item.dict()
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/api/inventory/{id}")
def delete_inventory_item(id: int):
    global mock_inventory
    mock_inventory = [item for item in mock_inventory if item["id"] != id]
    return {"message": "Item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts():
    return mock_alerts

@app.post("/api/alerts", response_model=Alert)
def create_alert(alert: Alert):
    alert.id = len(mock_alerts) + 1
    mock_alerts.append(alert.dict())
    return alert

@app.delete("/api/alerts/{id}")
def delete_alert(id: int):
    global mock_alerts
    mock_alerts = [alert for alert in mock_alerts if alert["id"] != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
def get_sales_trends():
    return mock_sales_trends

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)