from pydantic import BaseModel


class Review(BaseModel):
    id: int = None
    product_id: str
    user_id: str
    reviewerName: str = None
    helpful: str = None
    reviewText: str = None
    overall: int
    summary: str = None
    unixReviewTime: str = None
    reviewTime: str = None

    class Config:
        orm_mode = True