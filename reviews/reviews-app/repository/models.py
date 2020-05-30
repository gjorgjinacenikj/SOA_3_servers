from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String)
    user_id = Column(String)
    reviewerName = Column(String)
    helpful = Column(String)
    reviewText = Column(Text)
    overall = Column(Integer)
    summary = Column(Text)
    unixReviewTime = Column(String)
    reviewTime = Column(String)
