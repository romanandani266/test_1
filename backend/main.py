from fastapi import FastAPI, HTTPException, Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

mock_users = {
    "admin": {"username": "admin", "role": "admin"},
    "manager": {"username": "manager", "role": "manager"},
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in mock_users:
        return mock_users[token]
    raise HTTPException(status_code=401, detail="Invalid token")

class LoginRequest(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
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

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    if request.username in mock_users and request.password == "password":
        return {"token": request.username, "role": mock_users[request.username]["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory(filter: Optional[str] = Query(None)):
    inventory = [
        {"product_id": 1, "product_name": "Product A", "category": "Category 1", "price": 10.0, "quantity": 100},
        {"product_id": 2, "product_name": "Product B", "category": "Category 2", "price": 20.0, "quantity": 50},
    ]
    if filter:
        inventory = [item for item in inventory if filter.lower() in item["product_name"].lower()]
    return inventory

@app.post("/api/inventory")
async def add_inventory(item: InventoryItem):
    return {"message": "Inventory item added successfully", "item": item}

@app.put("/api/inventory/{id}")
async def update_inventory(id: int = Path(...), item: InventoryItem = Depends()):
    return {"message": f"Inventory item with ID {id} updated successfully", "item": item}

@app.delete("/api/inventory/{id}")
async def delete_inventory(id: int = Path(...)):
    return {"message": f"Inventory item with ID {id} deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    alerts = [
        {"alert_id": 1, "product_id": 1, "threshold": 20, "status": "active"},
        {"alert_id": 2, "product_id": 2, "threshold": 10, "status": "inactive"},
    ]
    return alerts

@app.post("/api/alerts")
async def create_alert(alert: Alert):
    return {"message": "Alert created successfully", "alert": alert}

@app.delete("/api/alerts/{id}")
async def delete_alert(id: int = Path(...)):
    return {"message": f"Alert with ID {id} deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrendReport])
async def get_sales_trends():
    trends = [
        {"product_id": 1, "product_name": "Product A", "sales_trend": "Increasing"},
        {"product_id": 2, "product_name": "Product B", "sales_trend": "Decreasing"},
    ]
    return trends