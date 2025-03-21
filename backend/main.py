from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4

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
    {"product_id": str(uuid4()), "name": "Product A", "category": "Category 1", "stock_level": 100, "last_updated": "2023-10-01T12:00:00Z"},
    {"product_id": str(uuid4()), "name": "Product B", "category": "Category 2", "stock_level": 50, "last_updated": "2023-10-01T12:00:00Z"},
]

mock_users = [
    {"user_id": str(uuid4()), "username": "admin", "password": "admin123", "role": "admin"},
    {"user_id": str(uuid4()), "username": "manager", "password": "manager123", "role": "warehouse_manager"},
]

class InventoryItem(BaseModel):
    product_id: str
    name: str
    category: str
    stock_level: int
    last_updated: str

class RestockingAlert(BaseModel):
    product_id: str
    threshold: int

class SalesTrendRequest(BaseModel):
    start_date: str
    end_date: str
    product_id: Optional[str]

class LoginRequest(BaseModel):
    username: str
    password: str

class NotificationRequest(BaseModel):
    product_id: str
    message: str
    type: str

def get_current_user(token: str):
    user = next((user for user in mock_users if user["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(product_id: Optional[str] = None, category: Optional[str] = None, token: str = Depends(get_current_user)):
    if token["role"] not in ["admin", "warehouse_manager", "retail_partner"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    filtered_inventory = mock_inventory
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item["product_id"] == product_id]
    if category:
        filtered_inventory = [item for item in filtered_inventory if item["category"] == category]
    if not filtered_inventory:
        raise HTTPException(status_code=404, detail="No inventory found")
    return filtered_inventory

@app.post("/api/alerts/restocking")
def create_restocking_alert(alert: RestockingAlert, token: str = Depends(get_current_user)):
    if token["role"] not in ["admin", "warehouse_manager"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Restocking alert created/updated successfully", "alert": alert}

@app.get("/api/sales/trends")
def get_sales_trends(request: SalesTrendRequest, token: str = Depends(get_current_user)):
    if token["role"] not in ["admin", "warehouse_manager", "retail_partner"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Sales trends fetched successfully", "data": {"start_date": request.start_date, "end_date": request.end_date, "product_id": request.product_id}}

@app.post("/api/auth/login")
def login(request: LoginRequest):
    user = next((user for user in mock_users if user["username"] == request.username and user["password"] == request.password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user["username"], "role": user["role"]}

@app.post("/api/notifications")
def send_notification(notification: NotificationRequest, token: str = Depends(get_current_user)):
    if token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Notification sent successfully", "notification": notification}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)