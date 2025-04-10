from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

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

mock_inventory = []
mock_alerts = []
mock_sales = []
mock_users = [{"username": "admin", "password": "admin123"}]

class Inventory(BaseModel):
    inventory_id: UUID
    product_id: UUID
    location_id: UUID
    stock_level: int
    supplier_id: UUID
    last_updated: datetime

class Alert(BaseModel):
    alert_id: UUID
    product_id: UUID
    location_id: UUID
    threshold: int
    current_stock: int
    alert_date: datetime

class Sale(BaseModel):
    sale_id: UUID
    product_id: UUID
    location_id: UUID
    sale_date: datetime
    quantity_sold: int

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(request: LoginRequest):
    for user in mock_users:
        if user["username"] == request.username and user["password"] == request.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/api/inventory", response_model=List[Inventory])
def get_inventory(location_id: Optional[UUID] = None, product_id: Optional[UUID] = None):
    filtered_inventory = mock_inventory
    if location_id:
        filtered_inventory = [item for item in filtered_inventory if item.location_id == location_id]
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item.product_id == product_id]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory data found for the given filters.")
    return filtered_inventory

@app.post("/api/inventory", response_model=Inventory)
def add_inventory(inventory: Inventory):
    inventory.inventory_id = uuid4()
    inventory.last_updated = datetime.now()
    mock_inventory.append(inventory)
    return inventory

@app.get("/api/alerts", response_model=List[Alert])
def get_alerts(location_id: Optional[UUID] = None, product_id: Optional[UUID] = None):
    filtered_alerts = mock_alerts
    if location_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert.location_id == location_id]
    if product_id:
        filtered_alerts = [alert for alert in filtered_alerts if alert.product_id == product_id]
    if not filtered_alerts:
        raise HTTPException(status_code=404, detail="No alerts found for the given filters.")
    return filtered_alerts

@app.put("/api/alerts", response_model=Alert)
def update_alert_threshold(alert_id: UUID, threshold: int):
    for alert in mock_alerts:
        if alert.alert_id == alert_id:
            alert.threshold = threshold
            return alert
    raise HTTPException(status_code=404, detail="Alert not found.")

@app.get("/api/sales-trends")
def get_sales_trends(start_date: str, end_date: str, product_id: Optional[UUID] = None):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    filtered_sales = [
        sale for sale in mock_sales 
        if start_date_obj <= sale.sale_date <= end_date_obj
    ]
    if product_id:
        filtered_sales = [sale for sale in filtered_sales if sale.product_id == product_id]
    if not filtered_sales:
        raise HTTPException(status_code=404, detail="No sales data found for the given filters.")
    trends = {
        "total_sales": sum(sale.quantity_sold for sale in filtered_sales),
        "average_sales": sum(sale.quantity_sold for sale in filtered_sales) / len(filtered_sales) if filtered_sales else 0,
        "peak_sales_period": "Mock Peak Period"
    }
    return trends

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
