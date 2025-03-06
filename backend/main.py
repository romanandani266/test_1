from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

mock_inventory = []
mock_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"}
}

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class InventoryItem(BaseModel):
    product_id: int
    name: str
    category: str
    quantity: int
    restock_threshold: int

def authenticate_user(username: str, password: str):
    user = mock_users.get(username)
    if not user or not (user["password"] == password):
        return False
    return user

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
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = mock_users.get(token_data.username)
    if user is None:
        raise credentials_exception
    return User(username=user["username"], role=user["role"])

@app.post("/api/auth/login", response_model=Token)
def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Successfully logged out"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(
    product_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    token: str = Depends(get_current_user),
):
    filtered_inventory = mock_inventory
    if product_id:
        filtered_inventory = [item for item in filtered_inventory if item.product_id == product_id]
    if category:
        filtered_inventory = [item for item in filtered_inventory if item.category == category]
    return filtered_inventory

@app.post("/api/inventory", response_model=InventoryItem)
def add_inventory(item: InventoryItem, token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to add inventory")
    mock_inventory.append(item)
    return item

@app.post("/api/inventory/alerts")
def restocking_alerts(token: str = Depends(get_current_user)):
    alerts = [
        {
            "product_id": item.product_id,
            "name": item.name,
            "message": "Restock needed"
        }
        for item in mock_inventory if item.quantity < item.restock_threshold
    ]
    return {"alerts": alerts}

@app.get("/api/inventory/sales-trends")
def sales_trends(token: str = Depends(get_current_user)):
    return {"message": "Sales trend analysis not implemented yet"}