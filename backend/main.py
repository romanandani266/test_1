from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
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

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {}
audit_logs = []

class User(BaseModel):
    username: str
    role: str
    password: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    return users_db.get(username)

def log_action(action: str, username: str):
    audit_logs.append({"timestamp": datetime.utcnow(), "action": action, "username": username})

@app.post("/register")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = {"username": user.username, "role": user.role, "password": get_password_hash(user.password)}
    log_action("register", user.username)
    return {"message": "User registered successfully"}

@app.post("/login")
def login_for_access_token(login_request: LoginRequest):
    user = get_user(login_request.username)
    if not user or not verify_password(login_request.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user["username"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    log_action("login", user["username"])
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.put("/users/{username}")
def update_user(username: str, user_update: UserUpdate, token: str):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.role:
        user["role"] = user_update.role
    if user_update.password:
        user["password"] = get_password_hash(user_update.password)
    log_action("update_user", username)
    return {"message": "User updated successfully"}

@app.delete("/users/{username}")
def delete_user(username: str, token: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[username]
    log_action("delete_user", username)
    return {"message": "User deleted successfully"}

@app.get("/audit-logs")
def get_audit_logs(token: str):
    return audit_logs

@app.get("/privacy-policy")
def get_privacy_policy():
    return {"policy": "We collect only necessary data for system functionality. Users have the right to access, modify, or delete their data."}

@app.post("/delete-account")
def delete_account(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if username not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        del users_db[username]
        log_action("delete_account", username)
        return {"message": "Account deleted successfully"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")