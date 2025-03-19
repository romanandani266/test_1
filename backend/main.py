from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

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

class Blog(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    image_url: HttpUrl
    created_at: Optional[datetime] = None

class LoginRequest(BaseModel):
    username: str
    password: str

blogs = []
blog_id_counter = 1

users = {"admin": "password123"}

@app.post("/login")
def login(request: LoginRequest):
    if request.username in users and users[request.username] == request.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    blog = next((blog for blog in blogs if blog.id == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=Blog)
def create_blog(blog: Blog):
    global blog_id_counter
    blog.id = blog_id_counter
    blog.created_at = datetime.now()
    blogs.append(blog)
    blog_id_counter += 1
    return blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, updated_blog: Blog):
    blog = next((blog for blog in blogs if blog.id == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = updated_blog.title
    blog.content = updated_blog.content
    blog.image_url = updated_blog.image_url
    return blog

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    global blogs
    blog = next((blog for blog in blogs if blog.id == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs = [b for b in blogs if b.id != blog_id]
    return {"message": "Blog deleted successfully"}