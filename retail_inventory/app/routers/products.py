from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, database, auth

router = APIRouter()

@router.get("/", response_model=list[schemas.ProductCreate])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.ProductCreate)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: schemas.UserCreate = Depends(auth.get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.create_product(db=db, product=product)