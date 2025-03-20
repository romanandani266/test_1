from fastapi import FastAPI, HTTPException
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

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: HttpUrl

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class Blog(BlogBase):
    id: int
    created_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

blogs = []
blog_id_counter = 1

users = {"admin": "password123"}

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = Blog(
        id=blog_id_counter,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at=datetime.now()
    )
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, blog_update: BlogUpdate):
    for blog in blogs:
        if blog.id == blog_id:
            if blog_update.title is not None:
                blog.title = blog_update.title
            if blog_update.content is not None:
                blog.content = blog_update.content
            if blog_update.image_url is not None:
                blog.image_url = blog_update.image_url
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    global blogs
    blogs = [blog for blog in blogs if blog.id != blog_id]
    return {"message": "Blog deleted successfully"}

@app.post("/login")
def login(login_request: LoginRequest):
    if login_request.username in users and users[login_request.username] == login_request.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")