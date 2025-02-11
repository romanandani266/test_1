from fastapi import FastAPI
from .routers import auth, products

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Inventory Management System"}