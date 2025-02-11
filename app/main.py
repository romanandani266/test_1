from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, products, inventory, sales

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(sales.router)
