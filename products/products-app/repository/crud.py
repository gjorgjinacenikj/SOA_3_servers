from typing import List

import pybreaker
from sqlalchemy.orm import Session

from . import models

db_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=20,
)

@db_circuit_breaker
def get_product_by_asin(db: Session, asin: str):
    return db.query(models.Product).filter(models.Product.asin == asin).first()

@db_circuit_breaker
def get_products(db: Session, skip: int = 0, limit: int = None) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()

@db_circuit_breaker
def create_product(db: Session, new_product:any):
    db_product = models.Product(**new_product.to_dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
