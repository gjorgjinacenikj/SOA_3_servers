from typing import List

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository import crud, schemas
from repository.database import engine, get_db


product_router = APIRouter()


@product_router.get("/products/{asin}", response_model=schemas.Product)
async def get_product(asin, db: Session = Depends(get_db)):
    return crud.get_product_by_asin ( db, asin)


@product_router.get("/products", response_model=List[schemas.Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip,limit)


@product_router.get("/writeProducts")
async def writeProducts(db: Session = Depends(get_db)):
    products = pd.read_csv('repository/data/meta_office.csv', index_col=[0])
    products.to_sql('products', con=engine, if_exists='append', index=False)

