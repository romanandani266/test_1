from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    description: str
    price: float
    available: bool

class UpdateItem(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    available: bool = None

users = {"admin": "password123"}
items = [
    {"id": 1, "name": "Item 1", "description": "Description 1", "price": 10.0, "available": True},
    {"id": 2, "name": "Item 2", "description": "Description 2", "price": 20.0, "available": False},
]

@app.post("/login")
def login(user: User):
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/items")
def get_items():
    return {"items": items}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def create_item(item: Item):
    for existing_item in items:
        if existing_item["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item.dict())
    return {"message": "Item created successfully", "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    for existing_item in items:
        if existing_item["id"] == item_id:
            if item.name is not None:
                existing_item["name"] = item.name
            if item.description is not None:
                existing_item["description"] = item.description
            if item.price is not None:
                existing_item["price"] = item.price
            if item.available is not None:
                existing_item["available"] = item.available
            return {"message": "Item updated successfully", "item": existing_item}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            deleted_item = items.pop(index)
            return {"message": "Item deleted successfully", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")