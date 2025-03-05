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

class User(BaseModel):
    username: str
    password: str

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    available: bool

users = {"admin": "password123"}
items = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.post("/login")
def login(user: User):
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful", "username": user.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/items", response_model=List[Item])
def get_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
def create_item(item: Item):
    for existing_item in items:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")