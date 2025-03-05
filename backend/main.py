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

products = []
users = {"admin": "password123"}

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Inventory Management System API"}

@app.post("/login")
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password
    if username in users and users[username] == password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/products", response_model=List[Product])
def get_all_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", response_model=Product)
def create_product(product: Product):
    for existing_product in products:
        if existing_product.id == product.id:
            raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(product)
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: UpdateProduct):
    for product in products:
        if product.id == product_id:
            if updated_product.name is not None:
                product.name = updated_product.name
            if updated_product.description is not None:
                product.description = updated_product.description
            if updated_product.price is not None:
                product.price = updated_product.price
            if updated_product.stock is not None:
                product.stock = updated_product.stock
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}/stock", response_model=dict)
def check_stock(product_id: int):
    for product in products:
        if product.id == product_id:
            return {"product_id": product_id, "stock": product.stock}
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/{product_id}/restock", response_model=dict)
def restock_product(product_id: int, quantity: int):
    for product in products:
        if product.id == product_id:
            product.stock += quantity
            return {"message": "Product restocked successfully", "new_stock": product.stock}
    raise HTTPException(status_code=404, detail="Product not found")