import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import Product, Base
from .db_creds import user,password,dbname

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/{dbname}".format(user=user,password=password,dbname=dbname)
#SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

def initialize_database():
    Base.metadata.drop_all(bind=engine, tables=[Product.__table__])
    print("Creating")
    Base.metadata.create_all(engine)

    product1 = Product()
    product1.title = 'Product1'
    product1.description = 'Product1 description'
    product1.asin = 'product1'
    product1.imUrl = 'https://boxboysupplies.com/wp-content/uploads/2018/04/boxed-inn-12x9x6-shipping-box.jpg'
    product1.brand = 'Product1 brand'
    product1.categories = 'Product1 categories'
    product1.price = 10
    product1.related = 'Product1 related'
    product1.salesRank = 'Product1 sales rank'

    product2 = Product()
    product2.title = 'Product2'
    product2.description = 'Product2 description'
    product2.asin = 'product2'
    product2.imUrl = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSsZTdhlNG0NwHIDwDWbYmguyroD66gfc77BFKQtvzpNpuoOuMH&usqp=CAU'
    product2.brand = 'Product2 brand'
    product2.categories = 'Product2 categories'
    product2.price = 20
    product2.related = 'Product2 related'
    product2.salesRank = 'Product2 sales rank'
    

    session.add(product1)
    session.add(product2)
    session.commit()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()