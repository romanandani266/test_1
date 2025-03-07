from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InventoryItem(BaseModel):
    product_id: str
    location_id: str
    quantity: int

class RestockingAlert(BaseModel):
    product_id: str
    location_id: str
    threshold: int

class LoginRequest(BaseModel):
    username: str
    password: str

mock_inventory = [
    {"product_id": "prod-1", "location_id": "loc-1", "quantity": 100},
    {"product_id": "prod-2", "location_id": "loc-1", "quantity": 50},
]

mock_alerts = [
    {"product_id": "prod-1", "location_id": "loc-1", "threshold": 20},
]

mock_sales_trends = [
    {"product_id": "prod-1", "location_id": "loc-1", "sales_data": [10, 20, 30]},
]

mock_users = {
    "admin": "password123",
}

@app.post("/api/login")
def login(request: LoginRequest):
    if request.username in mock_users and mock_users[request.username] == request.password:
        return {"message": "Login successful", "username": request.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/api/inventory", response_model=List[InventoryItem])
def fetch_inventory(location_id: Optional[str] = None, product_id: Optional[str] = None):
    filtered_inventory = mock_inventory
    if location_id:
        filtered_inventory = [item for item in filtered_inventory if item["location_id"] == location_id]
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item["product_id"] == product_id]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory data found for the given filters.")
    return filtered_inventory

@app.put("/api/inventory", response_model=InventoryItem)
def update_inventory(item: InventoryItem):
    for inventory_item in mock_inventory:
        if inventory_item["product_id"] == item.product_id and inventory_item["location_id"] == item.location_id:
            inventory_item["quantity"] = item.quantity
            return inventory_item
    raise HTTPException(status_code=404, detail="Inventory item not found.")

@app.get("/api/alerts", response_model=List[RestockingAlert])
def fetch_alerts(location_id: Optional[str] = None):
    filtered_alerts = mock_alerts
    if location_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert["location_id"] == location_id]
    if not filtered_alerts:
        raise HTTPException(status_code=404, detail="No alerts found for the given location.")
    return filtered_alerts

@app.post("/api/alerts", response_model=RestockingAlert)
def create_alert(alert: RestockingAlert):
    for existing_alert in mock_alerts:
        if existing_alert["product_id"] == alert.product_id and existing_alert["location_id"] == alert.location_id:
            raise HTTPException(status_code=409, detail="Alert already exists for the given product and location.")
    mock_alerts.append(alert.dict())
    return alert

@app.get("/api/sales/trends")
def fetch_sales_trends(product_id: Optional[str] = None, location_id: Optional[str] = None):
    filtered_trends = mock_sales_trends
    if product_id:
        filtered_trends = [trend for trend in filtered_trends if trend["product_id"] == product_id]
    if location_id:
        filtered_trends = [trend for trend in filtered_trends if trend["location_id"] == location_id]
    if not filtered_trends:
        raise HTTPException(status_code=404, detail="No sales trend data found for the given filters.")
    return filtered_trends

@app.get("/")
def root():
    return {"message": "Welcome to the Retail Inventory Management System API!"}