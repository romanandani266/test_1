from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

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
    {
        "inventory_id": str(uuid4()),
        "product_id": str(uuid4()),
        "location_id": str(uuid4()),
        "product_name": "Pepsi",
        "stock_level": 100,
        "expiration_date": "2023-12-31",
    }
]

mock_alerts = []
mock_sales_trends = []
mock_users = [
    {"user_id": str(uuid4()), "username": "admin", "password": "admin123", "role": "admin"}
]

class Inventory(BaseModel):
    inventory_id: UUID
    product_id: UUID
    location_id: UUID
    product_name: str
    stock_level: int
    expiration_date: str

class Alert(BaseModel):
    product_id: UUID
    threshold: int
    location_id: Optional[UUID]

class SalesTrend(BaseModel):
    start_date: str
    end_date: str
    product_category: Optional[str]

class UserLogin(BaseModel):
    username: str
    password: str

class IntegrationData(BaseModel):
    system_id: str
    data_format: str
    inventory_data: dict

def authenticate_user(username: str, password: str):
    user = next((u for u in mock_users if u["username"] == username and u["password"] == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.get("/api/inventory", response_model=List[Inventory])
async def get_inventory(location_id: Optional[str] = Query(None), product_category: Optional[str] = Query(None)):
    filtered_inventory = mock_inventory
    if location_id:
        filtered_inventory = [item for item in filtered_inventory if item["location_id"] == location_id]
    if product_category:
        filtered_inventory = [item for item in filtered_inventory if item["product_name"] == product_category]

    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory data found for the specified filters.")
    return filtered_inventory

@app.post("/api/alerts")
async def create_or_update_alert(alert: Alert, user: dict = Depends(authenticate_user)):
    if user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Permission denied.")

    mock_alerts.append(alert.dict())
    return {"message": "Alert created/updated successfully", "alert": alert}

@app.get("/api/sales-trends")
async def get_sales_trends(start_date: str, end_date: str, product_category: Optional[str] = Query(None)):
    sales_trends = [
        {"date": "2023-10-01", "sales": 100},
        {"date": "2023-10-02", "sales": 150},
    ]
    return {"start_date": start_date, "end_date": end_date, "product_category": product_category, "trends": sales_trends}

@app.post("/api/auth/login")
async def login(user_login: UserLogin):
    user = authenticate_user(user_login.username, user_login.password)
    return {"access_token": str(uuid4()), "role": user["role"]}

@app.post("/api/integration")
async def push_inventory_to_third_party(data: IntegrationData, user: dict = Depends(authenticate_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied.")

    return {"message": "Data pushed successfully", "integration_status": "success", "data": data}

@app.get("/")
async def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}