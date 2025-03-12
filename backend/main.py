from fastapi import FastAPI, HTTPException, Path, Body
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
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class UserLogin(BaseModel):
    username: str
    password: str

blogs = []
blog_id_counter = 1
users = {"admin": "password123"}

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int = Path(...)):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog)
def create_blog(blog_data: BlogCreate = Body(...)):
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
def update_blog(blog_id: int = Path(...), blog_data: BlogUpdate = Body(...)):
    for blog in blogs:
        if blog.id == blog_id:
            if blog_data.title is not None:
                blog.title = blog_data.title
            if blog_data.content is not None:
                blog.content = blog_data.content
            if blog_data.image_url is not None:
                blog.image_url = blog_data.image_url
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int = Path(...)):
    global blogs
    for blog in blogs:
        if blog.id == blog_id:
            blogs = [b for b in blogs if b.id != blog_id]
            return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/login")
def login(user: UserLogin = Body(...)):
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")