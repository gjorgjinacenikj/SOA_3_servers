from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    amount_paid = Column(Float)
    quantity =  Column(Integer)
    product_id = Column(String)
    user_id=Column(String)
    paid = Column(Boolean)
