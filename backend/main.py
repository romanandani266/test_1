from fastapi import FastAPI, HTTPException, Depends, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

mock_users = [{"username": "admin", "password": "password", "role": "admin"}]
mock_inventory = []
mock_alerts = []
mock_sales_trends = []

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token == "valid_token":
        return {"username": "test_user", "role": "admin"}
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/login")
async def login(user: User):
    for mock_user in mock_users:
        if user.username == mock_user["username"] and user.password == mock_user["password"]:
            return {"token": "valid_token", "role": mock_user["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory(category: Optional[str] = Query(None)):
    if category:
        return [item for item in mock_inventory if item["category"] == category]
    return mock_inventory

@app.post("/api/inventory")
async def add_inventory_item(item: InventoryItem):
    mock_inventory.append(item.dict())
    return {"message": "Inventory item added successfully"}

@app.put("/api/inventory/{id}")
async def update_inventory_item(id: int, item: InventoryItem):
    for i, inv_item in enumerate(mock_inventory):
        if inv_item["inventory_id"] == id:
            mock_inventory[i] = item.dict()
            return {"message": "Inventory item updated successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.delete("/api/inventory/{id}")
async def delete_inventory_item(id: int):
    global mock_inventory
    mock_inventory = [item for item in mock_inventory if item["inventory_id"] != id]
    return {"message": "Inventory item deleted successfully"}

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts():
    return mock_alerts

@app.post("/api/alerts")
async def create_alert(alert: Alert):
    mock_alerts.append(alert.dict())
    return {"message": "Alert created successfully"}

@app.delete("/api/alerts/{id}")
async def delete_alert(id: int):
    global mock_alerts
    mock_alerts = [alert for alert in mock_alerts if alert["alert_id"] != id]
    return {"message": "Alert deleted successfully"}

@app.get("/api/sales/trends", response_model=List[SalesTrend])
async def get_sales_trends():
    return mock_sales_trends

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)