from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

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

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    }
}

items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1", "price": 10.0, "on_offer": False},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2", "price": 20.0, "on_offer": True},
]

class User(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    on_offer: bool

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return None
    hashed_password = fake_hash_password(password)
    if hashed_password != fake_users_db[username]["hashed_password"]:
        return None
    return user

@app.post("/login")
async def login(user: UserLogin):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user": authenticated_user}

@app.get("/users/me", response_model=User)
async def read_users_me(username: str):
    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items.append(item.dict())
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items[index] = updated_item.dict()
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")