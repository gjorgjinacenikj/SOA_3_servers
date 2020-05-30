import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import Base, Review
from .db_creds import user,password,dbname

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/{dbname}".format(user=user,password=password,dbname=dbname)
#SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

def initialize_database():
    Base.metadata.drop_all(bind=engine, tables=[ Review.__table__])
    print("Creating")
    Base.metadata.create_all(engine)

    review1 = Review()
    review1.asin = 'review1'
    review1.user_id = 'user1'
    review1.product_id = 'product1'
    review1.helpful = 2
    review1.overall = 3
    review1.reviewerName = 'Review1 reviewerName'
    review1.reviewText = 'Review1 reviewText'
    review1.unixReviewTime = 'Review1 unixReviewTime'
    review1.summary = 'Review1 summary'
    

    session.add(review1)

    session.commit()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()