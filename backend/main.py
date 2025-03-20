from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List

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
users = {"admin": "password123"}
blog_id_counter = 1

class Blog(BaseModel):
    id: int
    title: str
    content: str
    image_url: HttpUrl
    created_at: datetime

class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: HttpUrl

class BlogUpdate(BaseModel):
    title: str
    content: str
    image_url: HttpUrl

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog)
def create_blog(blog_data: BlogCreate):
    global blog_id_counter
    new_blog = Blog(
        id=blog_id_counter,
        title=blog_data.title,
        content=blog_data.content,
        image_url=blog_data.image_url,
        created_at=datetime.now()
    )
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, blog_data: BlogUpdate):
    for blog in blogs:
        if blog.id == blog_id:
            blog.title = blog_data.title
            blog.content = blog_data.content
            blog.image_url = blog_data.image_url
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    global blogs
    for blog in blogs:
        if blog.id == blog_id:
            blogs = [b for b in blogs if b.id != blog_id]
            return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/login")
def login(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    if username in users and users[username] == password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")