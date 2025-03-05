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

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_active: bool

class LoginRequest(BaseModel):
    username: str
    password: str

items = []
users = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def create_item(item: Item):
    items.append(item.dict())
    return item

@app.post("/login")
def login(login_request: LoginRequest):
    for user in users:
        if user["username"] == login_request.username and user["password"] == login_request.password:
            return {"message": "Login successful", "user": user}
    raise HTTPException(status_code=401, detail="Invalid credentials")