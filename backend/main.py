from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

mock_inventory = []
mock_alerts = []
mock_sales_trends = []

class User(BaseModel):
    username: str
    password: str

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

class SalesTrend(BaseModel):
    product_id: int
    product_name: str
    sales_data: List[int]

@app.post("/api/auth/login")
async def login(user: User):
    if user.username == "admin" and user.password == "password":
        return {"token": "mock-jwt-token", "role": "admin"}
    elif user.username == "user" and user.password == "password":
        return {"token": "mock-jwt-token", "role": "user"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout():
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory():
    return mock_inventory

@app.post("/api/inventory")
async def add_inventory_item(item: InventoryItem):
    mock_inventory.append(item)
    return {"message": "Inventory item added successfully"}

@app.put("/api/inventory/{id}")
async def update_inventory_item(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory[i] = item
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
async def delete_inventory_item(id: int):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item.id == id:
            mock_inventory.pop(i)
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    return mock_alerts

@app.post("/api/alerts")
async def create_alert(alert: Alert):
    mock_alerts.append(alert)
    return {"message": "Alert created successfully"}

@app.delete("/api/alerts/{id}")
async def delete_alert(id: int):
    for i, alert in enumerate(mock_alerts):
        if alert.id == id:
            mock_alerts.pop(i)
            return {"message": "Alert deleted successfully"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends", response_model=List[SalesTrend])
async def get_sales_trends():
    return mock_sales_trends
