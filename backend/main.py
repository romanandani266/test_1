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

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

users = {"testuser": "testpassword"}
items = [
    {"id": 1, "name": "Item 1", "description": "Description 1", "price": 10.0},
    {"id": 2, "name": "Item 2", "description": "Description 2", "price": 20.0},
]

@app.post("/login", response_model=LoginResponse)
def login(user: User):
    if user.username in users and users[user.username] == user.password:
        token = f"token-{user.username}"
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/items", response_model=List[Item])
def get_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
def create_item(item: Item):
    for existing_item in items:
        if existing_item["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item.dict())
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    for item in items:
        if item["id"] == item_id:
            if item_update.name is not None:
                item["name"] = item_update.name
            if item_update.description is not None:
                item["description"] = item_update.description
            if item_update.price is not None:
                item["price"] = item_update.price
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")