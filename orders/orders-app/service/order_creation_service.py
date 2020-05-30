
from sqlalchemy.orm import Session

from repository.crud import create_order
from stripe.http_client import requests
from config import products_add

def create_and_save_order(db: Session, user_id, product_id, quantity):
    print("Saving order")


    product = requests.get("{0}/products/{1}".format(products_add, product_id)).json()
    price=product['price']
    order = create_order(db=db, user_id=user_id, product_id = product_id,
                         paid=False, quantity = quantity, amount_paid=quantity*price)
    return order, product
