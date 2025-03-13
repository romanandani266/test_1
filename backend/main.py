from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

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

blogs = []
users = {"admin": "password123"}
blog_id_counter = 1

class BlogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    image_url: HttpUrl

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

def find_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    return None

@app.get("/blogs", response_model=List[BlogResponse])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int):
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogResponse, status_code=201)
def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": datetime.utcnow(),
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
def update_blog(blog_id: int, updated_blog: BlogUpdate):
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.update(
        {
            "title": updated_blog.title,
            "content": updated_blog.content,
            "image_url": updated_blog.image_url,
        }
    )
    return blog

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    global blogs
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs = [b for b in blogs if b["id"] != blog_id]
    return {"message": "Blog deleted successfully"}

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    if username in users and users[username] == password:
        return {"message": "Login successful", "token": "dummy_token"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")