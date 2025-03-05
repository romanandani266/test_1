from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="User Management API", description="Backend API for managing users and authentication", version="1.0.0")

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

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class CreateUserRequest(BaseModel):
    name: str
    email: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

users = [
    User(id=1, name="John Doe", email="john.doe@example.com", is_active=True),
    User(id=2, name="Jane Smith", email="jane.smith@example.com", is_active=False)
]

fake_tokens = {
    "john.doe@example.com": "fake-token-john",
    "jane.smith@example.com": "fake-token-jane"
}

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
def create_user(user_request: CreateUserRequest):
    new_user = User(
        id=len(users) + 1,
        name=user_request.name,
        email=user_request.email,
        is_active=True
    )
    users.append(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_request: UpdateUserRequest):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_request.name is not None:
        user.name = user_request.name
    if user_request.email is not None:
        user.email = user_request.email
    if user_request.is_active is not None:
        user.is_active = user_request.is_active
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    global users
    users = [user for user in users if user.id != user_id]
    return {"message": "User deleted successfully"}

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    if login_request.email in fake_tokens and login_request.password == "password":
        return LoginResponse(message="Login successful", token=fake_tokens[login_request.email])
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}