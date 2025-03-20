from fastapi import FastAPI, HTTPException, Path, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from uuid import uuid4, UUID
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

blogs = {}
users = {"admin": {"username": "admin", "password": "admin123"}}

class BlogBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    image_url: Optional[HttpUrl]

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

async def validate_image(file: UploadFile):
    allowed_formats = ["image/jpeg", "image/png"]
    max_size = 5 * 1024 * 1024

    if file.content_type not in allowed_formats:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    if len(await file.read()) > max_size:
        raise HTTPException(status_code=400, detail="Image size exceeds 5MB.")
    await file.seek(0)

@app.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest = Body(...)):
    user = users.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "token": "dummy_token"}

@app.get("/blogs", response_model=List[BlogResponse])
async def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: UUID = Path(...)):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogResponse, status_code=201)
async def create_blog(blog: BlogCreate = Body(...), image: Optional[UploadFile] = File(None)):
    if image:
        await validate_image(image)

    blog_id = uuid4()
    now = datetime.utcnow()
    new_blog = {
        "id": blog_id,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": now,
        "updated_at": now
    }
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: UUID = Path(...), blog: BlogUpdate = Body(...), image: Optional[UploadFile] = File(None)):
    existing_blog = blogs.get(blog_id)
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if image:
        await validate_image(image)

    now = datetime.utcnow()
    updated_blog = {
        **existing_blog,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "updated_at": now
    }
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", status_code=204)
async def delete_blog(blog_id: UUID = Path(...)):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    del blogs[blog_id]
    return {"detail": "Blog deleted successfully"}