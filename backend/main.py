from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

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
    allow_headers=["*"],
)

class BlogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    image_url: HttpUrl

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    created_at: datetime

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

blogs = []
users = {"admin": "password123"}
blog_id_counter = 1

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": datetime.utcnow()
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, updated_blog: BlogUpdate):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    blog["title"] = updated_blog.title
    blog["content"] = updated_blog.content
    blog["image_url"] = updated_blog.image_url
    return blog

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    global blogs
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    blogs = [blog for blog in blogs if blog["id"] != blog_id]
    return {"message": "Blog post deleted successfully"}

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password
    if username in users and users[username] == password:
        return {"message": "Login successful", "token": "fake-jwt-token"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")