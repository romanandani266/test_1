from fastapi import FastAPI
from app.routers import auth, products, inventory, sales
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Retail Inventory Management System")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Inventory Management System"}