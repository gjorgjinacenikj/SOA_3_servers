from typing import List

import pybreaker
from sqlalchemy.orm import Session

from . import models, schemas

db_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=20,
)

@db_circuit_breaker
def get_reviews_by_product_id(db: Session, id: str) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.product_id == id).all()

@db_circuit_breaker
def get_reviews(db: Session, skip: int = 0, limit: int = None) -> List[models.Review]:
    return db.query(models.Review).offset(skip).limit(limit).all()

@db_circuit_breaker
def create_review(db: Session, new_review: schemas.Review) -> models.Review:
    db_review = models.Review(**new_review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
