from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock_level: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock_level: Optional[int] = None