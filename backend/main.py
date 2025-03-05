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
    category: str
    quantity: int
    restock_threshold: int
    price: float

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    restock_threshold: Optional[int] = None
    price: Optional[float] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Inventory Management System API"}

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
def update_product(product_id: int, product_update: UpdateProduct):
    for product in products:
        if product.id == product_id:
            if product_update.name is not None:
                product.name = product_update.name
            if product_update.category is not None:
                product.category = product_update.category
            if product_update.quantity is not None:
                product.quantity = product_update.quantity
            if product_update.restock_threshold is not None:
                product.restock_threshold = product_update.restock_threshold
            if product_update.price is not None:
                product.price = product_update.price
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/restock", response_model=List[Product])
def get_products_to_restock():
    restock_list = [product for product in products if product.quantity <= product.restock_threshold]
    return restock_list

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    if username in users and users[username] == password:
        return {"message": "Login successful", "token": "dummy_token"}
    raise HTTPException(status_code=401, detail="Invalid username or password")