from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {}

class User(BaseModel):
    username: str
    role: str
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    user = users_db.get(username)
    if user:
        return UserInDB(**user)
    return None

@app.post("/register", response_model=User)
async def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {
        "username": user.username,
        "role": user.role,
        "hashed_password": hashed_password,
    }
    return user

@app.get("/me", response_model=User)
async def read_users_me(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.delete("/delete-account")
async def delete_account(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if username in users_db:
            del users_db[username]
            return {"message": "Account deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/privacy-policy")
async def get_privacy_policy():
    return {
        "policy": "We collect only necessary data for system functionality. You have the right to access, modify, or delete your data. We do not share your data with third parties without consent."
    }

@app.post("/request-data-deletion")
async def request_data_deletion(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": "Your data deletion request has been received and will be processed within 30 days."}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/opt-out")
async def opt_out_data_sharing(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": "You have successfully opted out of data sharing."}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

audit_logs = []

@app.get("/audit-logs")
async def get_audit_logs(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = get_user(username)
        if user.role != "admin":
            raise HTTPException(status_code=403, detail="Access forbidden")
        return audit_logs
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/log-action")
async def log_action(action: str, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        audit_logs.append({"user": username, "action": action, "timestamp": datetime.utcnow()})
        return {"message": "Action logged successfully"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")