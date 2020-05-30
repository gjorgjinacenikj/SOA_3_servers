from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    imUrl = Column(String)
    related = Column(Text)
    salesRank = Column(String)
    categories = Column(String)
    brand = Column(String)
    price = Column(Float)
