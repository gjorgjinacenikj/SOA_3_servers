from typing import List

import pandas as pd
import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from repository import crud, schemas
from repository.database import engine, get_db
from config import orders_add

review_router = APIRouter()
@review_router.get("/reviews", response_model=List[schemas.Review])
async def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reviews ( db, skip, limit)


@review_router.post("/reviews", response_model=schemas.Review)
async def create_review(review: schemas.Review, request: Request, db: Session = Depends(get_db)):
    has_user_bought_product = requests.get("{0}/order?user_id={1}&product_id={2}".format(orders_add, review.user_id, review.product_id)).json()
    if not has_user_bought_product:
        raise HTTPException(status_code=500, detail='You have to buy the product before you review it')
    user_id = request.headers['X-Consumer-Custom-ID']
    review.user_id=user_id
    return crud.create_review(db, review)

@review_router.get("/reviews")
async def getReviewForProduct(product_id, db: Session = Depends(get_db)) -> List[schemas.Review]:
    return crud.get_reviews_by_product_id (db=db, id=product_id)


@review_router.get("/writeReviews")
async def writeReviews(db: Session = Depends(get_db)):
    reviews = pd.read_csv('repository/data/office_both_set.csv', index_col=[0])
    existing_reviews = set(['{0}_{1}'.format(review.reviewerID, review.asin) for review in crud.get_reviews(db)])
    for index, row in reviews.iterrows():
        if not '{0}_{1}'.format(row['reviewerID'], row['asin']) in existing_reviews:
            crud.create_review(db, row)
            print(row['asin'])