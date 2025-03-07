from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import uuid
import os

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

blogs = {}
users = {}

class Blog(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str] = None
    created_at: str
    updated_at: str

class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    email: str
    password_hash: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def generate_id():
    return str(uuid.uuid4())

@app.get("/blogs", response_model=List[Blog])
def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blogs[blog_id]

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    blog_id = generate_id()
    new_blog = Blog(
        id=blog_id,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z",
    )
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: str, blog_update: BlogUpdate):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    existing_blog = blogs[blog_id]
    updated_blog = existing_blog.copy(update=blog_update.dict(exclude_unset=True))
    updated_blog.updated_at = "2023-01-01T00:00:00Z"
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    del blogs[blog_id]
    return JSONResponse(status_code=204, content={"message": "Blog deleted successfully"})

@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    allowed_extensions = {"jpg", "jpeg", "png", "gif"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format. Allowed formats: jpg, jpeg, png, gif")
    file_location = f"images/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"image_url": f"/{file_location}"}

@app.post("/register", response_model=User, status_code=201)
def register_user(user: UserCreate):
    user_id = generate_id()
    if any(u.email == user.email for u in users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        password_hash=user.password,
    )
    users[user_id] = new_user
    return new_user

@app.post("/login")
def login_user(user: UserLogin):
    for u in users.values():
        if u.email == user.email and u.password_hash == user.password:
            return {"message": "Login successful", "user_id": u.id}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/dark-mode")
def toggle_dark_mode(enabled: bool = Form(...)):
    return {"dark_mode_enabled": enabled}