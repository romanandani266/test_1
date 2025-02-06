from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock_level: int

class SaleCreate(BaseModel):
    product_id: UUID
    quantity_sold: int
    sale_date: datetime
