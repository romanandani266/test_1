from fastapi import FastAPI, HTTPException, Path
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
    image_url: HttpUrl = Field(...)

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
def get_blog(blog_id: int = Path(...)):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog post not found")

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
def update_blog(blog_id: int, updated_blog: BlogUpdate):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            blogs[index] = Blog(
                id=blog.id,
                title=updated_blog.title,
                content=updated_blog.content,
                image_url=updated_blog.image_url,
                created_at=blog.created_at
            )
            return blogs[index]
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            del blogs[index]
            return
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    if login_request.username in users and users[login_request.username] == login_request.password:
        token = f"fake-token-for-{login_request.username}"
        return LoginResponse(message="Login successful", token=token)
    raise HTTPException(status_code=401, detail="Invalid username or password")