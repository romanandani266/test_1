from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

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

users_db = {}
entities_db = {}
jwt_blacklist = set()

class User(BaseModel):
    id: int
    username: str
    password: str
    is_admin: bool = False

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

class Entity(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or token in jwt_blacklist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return users_db.get(username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_admin_user(current_user: User):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user

@app.post("/api/auth/register", response_model=UserOut)
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.dict()
    return user

@app.post("/api/auth/login", response_model=Token)
def login_user(login_request: LoginRequest):
    user = users_db.get(login_request.username)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
def logout_user(token: str):
    jwt_blacklist.add(token)
    return {"message": "Successfully logged out"}

@app.get("/api/users", response_model=List[UserOut])
def get_all_users(token: str):
    current_user = get_current_user(token)
    get_admin_user(current_user)
    return [UserOut(**user) for user in users_db.values()]

@app.get("/api/users/{id}", response_model=UserOut)
def get_user(id: int, token: str):
    current_user = get_current_user(token)
    for user in users_db.values():
        if user["id"] == id:
            return UserOut(**user)
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/api/users/{id}", response_model=UserOut)
def update_user(id: int, updated_user: User, token: str):
    current_user = get_current_user(token)
    for username, user in users_db.items():
        if user["id"] == id:
            if current_user["id"] != id and not current_user["is_admin"]:
                raise HTTPException(status_code=403, detail="Permission denied")
            users_db[username].update(updated_user.dict())
            return UserOut(**users_db[username])
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/api/users/{id}")
def delete_user(id: int, token: str):
    current_user = get_current_user(token)
    get_admin_user(current_user)
    for username, user in list(users_db.items()):
        if user["id"] == id:
            del users_db[username]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/entities", response_model=Entity)
def create_entity(entity: Entity, token: str):
    current_user = get_current_user(token)
    entity.owner_id = current_user["id"]
    entities_db[entity.id] = entity.dict()
    return entity

@app.get("/api/entities", response_model=List[Entity])
def get_all_entities(token: str):
    current_user = get_current_user(token)
    return [Entity(**entity) for entity in entities_db.values()]

@app.get("/api/entities/{id}", response_model=Entity)
def get_entity(id: int, token: str):
    current_user = get_current_user(token)
    entity = entities_db.get(id)
    if not entity or entity["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Entity not found")
    return Entity(**entity)

@app.put("/api/entities/{id}", response_model=Entity)
def update_entity(id: int, updated_entity: Entity, token: str):
    current_user = get_current_user(token)
    entity = entities_db.get(id)
    if not entity or entity["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Entity not found")
    entities_db[id].update(updated_entity.dict())
    return Entity(**entities_db[id])

@app.delete("/api/entities/{id}")
def delete_entity(id: int, token: str):
    current_user = get_current_user(token)
    entity = entities_db.get(id)
    if not entity or entity["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Entity not found")
    del entities_db[id]
    return {"message": "Entity deleted successfully"}