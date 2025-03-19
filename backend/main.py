from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import imghdr

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

blogs = {}
users = {}
comments = {}
likes = {}

class Blog(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    image_url: Optional[str] = None
    created_at: str
    updated_at: str

class BlogCreate(BaseModel):
    user_id: str
    title: str
    content: str
    image_url: Optional[str] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Comment(BaseModel):
    id: str
    blog_id: str
    user_id: str
    content: str
    created_at: str

class CommentCreate(BaseModel):
    blog_id: str
    user_id: str
    content: str

class Like(BaseModel):
    id: str
    blog_id: str
    user_id: str
    created_at: str

class LikeCreate(BaseModel):
    blog_id: str
    user_id: str

def validate_image(file: UploadFile):
    valid_image_types = ["jpeg", "png", "gif"]
    file_type = imghdr.what(file.file)
    if file_type not in valid_image_types:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG, PNG, and GIF are allowed.")
    return file_type

@app.post("/users/register", response_model=User)
def register_user(user: User):
    if user.email in [u.email for u in users.values()]:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid4())
    new_user = User(id=user_id, username=user.username, email=user.email, password=user.password)
    users[user_id] = new_user
    return new_user

@app.post("/users/login")
def login_user(user: UserLogin):
    for u in users.values():
        if u.email == user.email and u.password == user.password:
            return {"message": "Login successful", "user_id": u.id}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/blogs", response_model=List[Blog])
def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: str):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=Blog)
def create_blog(blog: BlogCreate):
    blog_id = str(uuid4())
    new_blog = Blog(
        id=blog_id,
        user_id=blog.user_id,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z",
    )
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: str, blog_update: BlogUpdate):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    updated_blog = blog.copy(update=blog_update.dict(exclude_unset=True))
    updated_blog.updated_at = "2023-01-01T00:00:00Z"
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", response_model=dict)
def delete_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    del blogs[blog_id]
    return {"message": "Blog deleted successfully"}

@app.post("/comments", response_model=Comment)
def create_comment(comment: CommentCreate):
    comment_id = str(uuid4())
    new_comment = Comment(
        id=comment_id,
        blog_id=comment.blog_id,
        user_id=comment.user_id,
        content=comment.content,
        created_at="2023-01-01T00:00:00Z",
    )
    comments[comment_id] = new_comment
    return new_comment

@app.get("/blogs/{blog_id}/comments", response_model=List[Comment])
def get_comments(blog_id: str):
    return [c for c in comments.values() if c.blog_id == blog_id]

@app.post("/likes", response_model=Like)
def like_blog(like: LikeCreate):
    like_id = str(uuid4())
    new_like = Like(
        id=like_id,
        blog_id=like.blog_id,
        user_id=like.user_id,
        created_at="2023-01-01T00:00:00Z",
    )
    likes[like_id] = new_like
    return new_like

@app.get("/blogs/{blog_id}/likes", response_model=int)
def get_likes(blog_id: str):
    return len([l for l in likes.values() if l.blog_id == blog_id])

@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    validate_image(file)
    return {"filename": file.filename, "message": "Image uploaded successfully"}

@app.get("/")
def root():
    return {"message": "Welcome to the Modern Blog Platform API"}