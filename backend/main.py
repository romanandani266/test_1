from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt

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

users_db = {}
data_db = {}
refresh_tokens_db = {}

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

class DataEntry(BaseModel):
    id: int
    user_id: int
    content: str

class DataUpdate(BaseModel):
    content: Optional[str]

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str):
    username = verify_token(token)
    user = next((user for user in users_db.values() if user["username"] == username), None)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/auth/register", response_model=User)
def register_user(user: User):
    if user.email in [u["email"] for u in users_db.values()]:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.username in [u["username"] for u in users_db.values()]:
        raise HTTPException(status_code=400, detail="Username already taken")
    users_db[user.id] = user.dict()
    return user

@app.post("/auth/login", response_model=Token)
def login_user(login_request: LoginRequest):
    user = next((u for u in users_db.values() if u["username"] == login_request.username), None)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/refresh", response_model=Token)
def refresh_token(token: str):
    username = verify_token(token)
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{id}", response_model=User)
def get_user(id: int, token: str):
    current_user = get_current_user(token)
    user = users_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{id}", response_model=User)
def update_user(id: int, user_update: UserUpdate, token: str):
    current_user = get_current_user(token)
    user = users_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(user_update.dict(exclude_unset=True))
    users_db[id] = user
    return user

@app.delete("/users/{id}")
def delete_user(id: int, token: str):
    current_user = get_current_user(token)
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[id]
    return {"detail": "User deleted successfully"}

@app.get("/data", response_model=List[DataEntry])
def get_data(token: str):
    current_user = get_current_user(token)
    return [data for data in data_db.values() if data["user_id"] == current_user["id"]]

@app.post("/data", response_model=DataEntry)
def create_data(data: DataEntry, token: str):
    current_user = get_current_user(token)
    data_db[data.id] = data.dict()
    return data

@app.get("/data/{id}", response_model=DataEntry)
def get_data_by_id(id: int, token: str):
    current_user = get_current_user(token)
    data = data_db.get(id)
    if not data or data["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.put("/data/{id}", response_model=DataEntry)
def update_data(id: int, data_update: DataUpdate, token: str):
    current_user = get_current_user(token)
    data = data_db.get(id)
    if not data or data["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Data not found")
    data.update(data_update.dict(exclude_unset=True))
    data_db[id] = data
    return data

@app.delete("/data/{id}")
def delete_data(id: int, token: str):
    current_user = get_current_user(token)
    data = data_db.get(id)
    if not data or data["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Data not found")
    del data_db[id]
    return {"detail": "Data deleted successfully"}