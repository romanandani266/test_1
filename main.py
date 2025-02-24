from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Optional

app = FastAPI()

DATABASE_URL = "postgresql://username:password@localhost/retail_inventory"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product = relationship("Product")

class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    threshold = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product")

class Sale(Base):
    __tablename__ = "sales"
    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    product = relationship("Product")

Base.metadata.create_all(bind=engine)

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/inventory")
def get_inventory(product_id: Optional[int] = None, category: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(Inventory)
    if product_id:
        query = query.filter(Inventory.product_id == product_id)
    if category:
        query = query.join(Product).filter(Product.category == category)
    return query.all()

@app.post("/api/inventory")
def add_inventory(item: dict, db: SessionLocal = Depends(get_db)):
    new_item = Inventory(**item)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Inventory item added", "item_id": new_item.inventory_id}

@app.put("/api/inventory/{id}")
def update_inventory(id: int, item: dict, db: SessionLocal = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.inventory_id == id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    for key, value in item.items():
        setattr(inventory_item, key, value)
    db.commit()
    return {"message": "Inventory item updated"}

@app.delete("/api/inventory/{id}")
def delete_inventory(id: int, db: SessionLocal = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.inventory_id == id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    db.delete(inventory_item)
    db.commit()
    return {"message": "Inventory item deleted"}

@app.get("/api/alerts")
def get_alerts(db: SessionLocal = Depends(get_db)):
    return db.query(Alert).all()

@app.post("/api/alerts")
def add_alert(alert: dict, db: SessionLocal = Depends(get_db)):
    new_alert = Alert(**alert)
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return {"message": "Alert created", "alert_id": new_alert.alert_id}

@app.delete("/api/alerts/{id}")
def delete_alert(id: int, db: SessionLocal = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.alert_id == id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted"}

@app.get("/api/sales/trends")
def get_sales_trends(start_date: Optional[Date] = None, end_date: Optional[Date] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(Sale)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    sales = query.all()
    return sales