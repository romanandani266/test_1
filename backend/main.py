from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

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

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_db = {
    "admin": {"username": "admin", "password_hash": "admin123", "role": "admin"},
    "user": {"username": "user", "password_hash": "user123", "role": "user"},
}

inventory_db = [
    {"id": 1, "name": "Item A", "quantity": 10, "price": 100.0},
    {"id": 2, "name": "Item B", "quantity": 5, "price": 50.0},
]

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role: str

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

class UserData(BaseModel):
    username: str
    role: str

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password_hash"] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        role: str = payload.get("role")
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

def get_current_admin_user(current_user: dict):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@app.post("/auth/login", response_model=Token)
def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/roles", response_model=List[str])
def get_roles(token: str):
    current_user = get_current_user(token)
    return [current_user["role"]]

@app.get("/inventory", response_model=List[InventoryItem])
def get_inventory(token: str):
    current_user = get_current_user(token)
    return inventory_db

@app.post("/inventory", response_model=InventoryItem)
def add_inventory(item: InventoryItem, token: str):
    current_user = get_current_user(token)
    get_current_admin_user(current_user)
    inventory_db.append(item.dict())
    return item

@app.put("/inventory/{id}", response_model=InventoryItem)
def update_inventory(id: int, item: InventoryItem, token: str):
    current_user = get_current_user(token)
    get_current_admin_user(current_user)
    for i, inv_item in enumerate(inventory_db):
        if inv_item["id"] == id:
            inventory_db[i] = item.dict()
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/inventory/{id}")
def delete_inventory(id: int, token: str):
    current_user = get_current_user(token)
    get_current_admin_user(current_user)
    for i, inv_item in enumerate(inventory_db):
        if inv_item["id"] == id:
            del inventory_db[i]
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/user/data", response_model=UserData)
def get_user_data(token: str):
    current_user = get_current_user(token)
    return {"username": current_user["username"], "role": current_user["role"]}

@app.delete("/user/data")
def delete_user_data(token: str):
    current_user = get_current_user(token)
    return {"detail": f"User data for {current_user['username']} has been deleted"}

@app.post("/user/opt-out")
def opt_out_data_sharing(token: str):
    current_user = get_current_user(token)
    return {"detail": f"User {current_user['username']} has opted out of data sharing"}