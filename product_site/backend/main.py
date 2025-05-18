from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from .models import Product
from .database import create_db_and_tables, get_session
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Product Store API is running!"}

@app.post("/products/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products/", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.in_stock = updated_product.in_stock

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return {"ok": True}
