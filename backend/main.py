from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
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

mock_inventory = [
    {"product_id": "1", "location_id": "101", "stock_level": 50, "threshold": 20},
    {"product_id": "2", "location_id": "102", "stock_level": 10, "threshold": 15},
]

mock_sales = [
    {"product_id": "1", "location_id": "101", "quantity_sold": 5, "sale_date": "2023-10-01"},
    {"product_id": "2", "location_id": "102", "quantity_sold": 3, "sale_date": "2023-10-02"},
]

class InventoryResponse(BaseModel):
    product_id: str
    location_id: str
    stock_level: int
    threshold: int

class RestockingAlertRequest(BaseModel):
    product_id: str
    current_stock: int
    threshold: int

class RestockingAlertResponse(BaseModel):
    status: str
    alert_id: str

class SalesTrendResponse(BaseModel):
    product_id: str
    sales_trends: List[dict]

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str

class ERPIntegrationRequest(BaseModel):
    erp_system: str
    inventory_data: List[dict]

class ERPIntegrationResponse(BaseModel):
    status: str
    integration_id: str

@app.get("/api/inventory", response_model=List[InventoryResponse])
def get_inventory(location_id: Optional[str] = None, product_id: Optional[str] = None):
    filtered_inventory = mock_inventory
    if location_id:
        filtered_inventory = [item for item in filtered_inventory if item["location_id"] == location_id]
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item["product_id"] == product_id]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory found for the given criteria")
    return filtered_inventory

@app.post("/api/alerts/restocking", response_model=RestockingAlertResponse)
def create_restocking_alert(alert_request: RestockingAlertRequest):
    if alert_request.current_stock >= alert_request.threshold:
        raise HTTPException(status_code=400, detail="Stock level is above the threshold")
    alert_id = f"alert_{datetime.now().timestamp()}"
    return {"status": "success", "alert_id": alert_id}

@app.get("/api/sales/trends", response_model=SalesTrendResponse)
def get_sales_trends(start_date: str, end_date: str, product_id: Optional[str] = None):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    filtered_sales = [sale for sale in mock_sales if start_date <= sale["sale_date"] <= end_date]
    if product_id:
        filtered_sales = [sale for sale in filtered_sales if sale["product_id"] == product_id]
    if not filtered_sales:
        raise HTTPException(status_code=404, detail="No sales data found for the given criteria")
    
    sales_trends = [{"date": sale["sale_date"], "quantity_sold": sale["quantity_sold"]} for sale in filtered_sales]
    return {"product_id": product_id or "all", "sales_trends": sales_trends}

@app.post("/api/integration/erp", response_model=ERPIntegrationResponse)
def integrate_with_erp(erp_request: ERPIntegrationRequest):
    if not erp_request.inventory_data:
        raise HTTPException(status_code=400, detail="Inventory data cannot be empty")
    integration_id = f"erp_{datetime.now().timestamp()}"
    return {"status": "success", "integration_id": integration_id}

@app.post("/api/auth/login", response_model=AuthResponse)
def login(auth_request: AuthRequest):
    if auth_request.username == "admin" and auth_request.password == "password":
        return {"access_token": "mock_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/")
def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}