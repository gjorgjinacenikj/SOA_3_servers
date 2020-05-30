from typing import List

import pybreaker
from sqlalchemy import Date
from sqlalchemy.orm import Session

from repository.repo_models import Order

from repository.repo_models import Base

db_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=10, listeners=[pybreaker.CircuitBreakerListener()])


@db_breaker
def get_orders(db: Session, skip: int = 0, limit: int = None) -> List[Order]:
    return __get_all(db, Order, skip, limit)


@db_breaker
def __get_all(db, what: Base, skip: int, limit: int):
    return db.query(what).offset(skip).limit(limit).all()


@db_breaker
def get_paid_order_by_user_and_product(db: Session, user_id: str, product_id: str):
    return db.query(Order).filter(
        Order.user_id == user_id and Order.product_id == product_id and Order.paid == True).first()


@db_breaker
def create_order(db: Session, user_id: int,
                 amount_paid: float,
                 product_id: int,
                 quantity: int,
                 paid: bool):
    order = Order(user_id=user_id, amount_paid=amount_paid, product_id=product_id, paid=paid, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@db_breaker
def get_order_by_id(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()
