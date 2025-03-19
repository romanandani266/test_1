from fastapi import FastAPI, HTTPException, Path, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
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
    allow_headers=["*"]
)

blogs = []
blog_id_counter = 1
users = {"test_user": "test_password"}

class Blog(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest):
    if login_request.username in users and users[login_request.username] == login_request.password:
        return {"access_token": "valid_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/blogs", response_model=List[Blog])
def get_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int = Path(...)):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog

@app.post("/blogs", response_model=Blog)
def create_blog(blog_data: BlogCreate):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog_data.title,
        "content": blog_data.content,
        "image_url": blog_data.image_url,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, blog_data: BlogUpdate):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    if blog_data.title:
        blog["title"] = blog_data.title
    if blog_data.content:
        blog["content"] = blog_data.content
    if blog_data.image_url:
        blog["image_url"] = blog_data.image_url
    blog["updated_at"] = datetime.utcnow()
    return blog

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    global blogs
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    blogs = [b for b in blogs if b["id"] != blog_id]
    return
