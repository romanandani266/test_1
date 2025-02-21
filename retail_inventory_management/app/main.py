from fastapi import FastAPI
from .routers import auth, products, inventory, sales

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])
