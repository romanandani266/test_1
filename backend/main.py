from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Product(BaseModel):
    product_id: int
    product_name: str
    description: Optional[str] = None
    created_at: datetime = datetime.now()

# Additional models and endpoints go here...