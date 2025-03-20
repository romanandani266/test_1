from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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

mock_inventory = [
    {"product_id": "1", "product_name": "Pepsi", "stock_level": 50, "warehouse_id": "101"},
    {"product_id": "2", "product_name": "Lays", "stock_level": 20, "warehouse_id": "102"},
]

mock_alerts = [
    {"alert_id": "1", "product_id": "2", "product_name": "Lays", "current_stock": 20, "threshold": 25},
]

mock_sales_trends = {
    "1": {"daily_sales": [10, 15, 20], "average_sales": 15, "predicted_demand": 18},
}

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_role: str

class InventoryItem(BaseModel):
    product_id: str
    product_name: str
    stock_level: int
    warehouse_id: str

class UpdateStockRequest(BaseModel):
    product_id: str
    warehouse_id: str
    new_stock_level: int

class Alert(BaseModel):
    alert_id: str
    product_id: str
    product_name: str
    current_stock: int
    threshold: int

class AcknowledgeAlertRequest(BaseModel):
    alert_id: str

class SalesTrendResponse(BaseModel):
    daily_sales: List[int]
    average_sales: float
    predicted_demand: int

@app.post("/api/auth/login", response_model=LoginResponse)
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        return {"token": "mock-jwt-token", "user_role": "admin"}
    elif request.username == "manager" and request.password == "password":
        return {"token": "mock-jwt-token", "user_role": "manager"}
    elif request.username == "staff" and request.password == "password":
        return {"token": "mock-jwt-token", "user_role": "staff"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/logout")
def logout(token: str):
    return {"message": "Logout successful"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(warehouse_id: Optional[str] = None, product_id: Optional[str] = None):
    filtered_inventory = mock_inventory
    if warehouse_id:
        filtered_inventory = [item for item in filtered_inventory if item["warehouse_id"] == warehouse_id]
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item["product_id"] == product_id]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory data found")
    return filtered_inventory

@app.post("/api/inventory/update")
def update_stock(request: UpdateStockRequest):
    for item in mock_inventory:
        if item["product_id"] == request.product_id and item["warehouse_id"] == request.warehouse_id:
            item["stock_level"] = request.new_stock_level
            return {"message": "Stock updated successfully"}
    raise HTTPException(status_code=404, detail="Product or warehouse not found")

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts(warehouse_id: Optional[str] = None):
    filtered_alerts = mock_alerts
    if warehouse_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert.get("warehouse_id") == warehouse_id]
    if not filtered_alerts:
        raise HTTPException(status_code=404, detail="No alerts available")
    return filtered_alerts

@app.post("/api/alerts/acknowledge")
def acknowledge_alert(request: AcknowledgeAlertRequest):
    for alert in mock_alerts:
        if alert["alert_id"] == request.alert_id:
            mock_alerts.remove(alert)
            return {"message": "Alert acknowledged"}
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/sales/trends", response_model=SalesTrendResponse)
def get_sales_trends(product_id: str, time_period: str):
    if product_id in mock_sales_trends:
        return mock_sales_trends[product_id]
    raise HTTPException(status_code=404, detail="No sales data available")