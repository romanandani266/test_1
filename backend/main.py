from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Define the allowed origins for CORS
origins = [
    "http://localhost:3000",
    "https://yourfrontend.com"
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Define the Blog model with required fields
class Blog(BaseModel):
    id: int
    title: str = Field(..., max_length=255)
    content: str
    image_url: HttpUrl
    created_at: datetime

# Define the BlogCreate model for creating new blogs
class BlogCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    image_url: HttpUrl

# Define the BlogUpdate model for updating existing blogs
class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str]
    image_url: Optional[HttpUrl]

# Define the LoginRequest model for user login
class LoginRequest(BaseModel):
    username: str
    password: str

# Initialize an empty list to store blogs
blogs = []

# Initialize a counter for assigning unique IDs to blogs
blog_id_counter = 1

# Define a dictionary to store user credentials
users = {"admin": "password123"}

# Endpoint to retrieve all blogs
@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

# Endpoint to retrieve a specific blog by its ID
@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog post not found")

# Endpoint to create a new blog
@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = Blog(
        id=blog_id_counter,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at=datetime.utcnow()
    )
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

# Endpoint to update an existing blog
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
    raise HTTPException(status_code=404, detail="Blog post not found")

# Endpoint to delete a blog by its ID
@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int):
    global blogs
    blogs = [blog for blog in blogs if blog.id != blog_id]
    return {"message": "Blog post deleted successfully"}

# Endpoint to handle user login
@app.post("/login")
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    if username in users and users[username] == password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# Root endpoint to welcome users to the API
@app.get("/")
def root():
    return {"message": "Welcome to the Modern Blog Platform API"}