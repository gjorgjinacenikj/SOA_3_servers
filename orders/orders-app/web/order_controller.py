from typing import List
import numpy as np
import pandas as pd
from fastapi import Depends, APIRouter
from fastapi import Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from repository import crud
from repository.crud import db_breaker, get_order_by_id
from repository.database import get_db

from service.order_creation_service import create_and_save_order

from repository.crud import get_paid_order_by_user_and_product
from service.service_models import Order

order_router = APIRouter()


templates = Jinja2Templates(directory="frontend")

@order_router.get(
    "/orders", response_model=List[Order],
    summary="Fetch all orders",
    description="Fetches all of the orders.")
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db, limit=100)


@order_router.get(
    "/create-order",
    summary="Create an order based on the package you selected",
    description="Creates an order based on the package you selected")
def create_order(user_id: str, product_id: str, quantity: int, request: Request, db: Session = Depends(get_db)):
    order, product = create_and_save_order(db, user_id, product_id, quantity)
    return templates.TemplateResponse("checkout.html", {"request": request, "amount": order.amount_paid,
                                                        "orderId": order.id, "productTitle": product['title'], "productQuantity": quantity})

@order_router.get("/order", summary="Checks whether a user has paid for a product")
def get_order(user_id: str, product_id: str, db:Session = Depends(get_db)):
    return get_paid_order_by_user_and_product(db, user_id=user_id, product_id=product_id) is not None


