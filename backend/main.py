from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
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

mock_inventory = {}
mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "manager": {"username": "manager", "password": "manager123", "role": "manager"},
    "viewer": {"username": "viewer", "password": "viewer123", "role": "viewer"},
}

class Product(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid4()))
    product_name: str
    description: Optional[str] = None
    price: Optional[float] = None
    stock_level: int
    threshold: int

class InventoryUpdate(BaseModel):
    product_id: str
    quantity: int

class NewProduct(BaseModel):
    product_name: str
    initial_stock: int
    description: Optional[str] = None
    price: Optional[float] = None

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login(login_request: LoginRequest):
    user = mock_users.get(login_request.username)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "role": user["role"]}

@app.get("/api/inventory", response_model=List[Product])
async def get_current_inventory(product_id: Optional[str] = Query(None)):
    if product_id:
        product = mock_inventory.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return [product]
    return list(mock_inventory.values())

@app.put("/api/inventory")
async def update_inventory(inventory_update: InventoryUpdate = Body(...)):
    product = mock_inventory.get(inventory_update.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock_level += inventory_update.quantity
    return {"message": "Inventory updated successfully", "product": product}

@app.post("/api/inventory")
async def add_new_product(new_product: NewProduct = Body(...)):
    product_id = str(uuid4())
    product = Product(
        product_id=product_id,
        product_name=new_product.product_name,
        description=new_product.description,
        price=new_product.price,
        stock_level=new_product.initial_stock,
        threshold=10
    )
    mock_inventory[product_id] = product
    return {"message": "Product added successfully", "product_id": product_id}

@app.delete("/api/inventory/{product_id}")
async def delete_product(product_id: str = Path(...)):
    product = mock_inventory.pop(product_id, None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.get("/api/sales-trends")
async def get_sales_trends():
    sales_trends = {
        "top_selling_products": ["Product A", "Product B"],
        "low_selling_products": ["Product C"],
        "predicted_demand": {"Product A": 100, "Product B": 50},
    }
    return sales_trends

@app.get("/api/notifications")
async def get_notifications():
    notifications = [
        {"product_id": "1", "message": "Stock is below threshold for Product A"},
        {"product_id": "2", "message": "Stock is below threshold for Product B"},
    ]
    return notifications

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
