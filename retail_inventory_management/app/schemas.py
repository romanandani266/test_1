from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class User(BaseModel):
    id: UUID
    email: str
    role: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock_level: int

class Product(BaseModel):
    id: UUID
    name: str
    category: str
    price: float
    stock_level: int

    class Config:
        orm_mode = True

class SaleCreate(BaseModel):
    product_id: UUID
    quantity_sold: int
    sale_date: datetime

class Sale(BaseModel):
    id: UUID
    product_id: UUID
    quantity_sold: int
    sale_date: datetime

    class Config:
        orm_mode = True