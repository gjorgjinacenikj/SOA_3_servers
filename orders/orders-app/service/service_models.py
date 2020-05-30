from pydantic import BaseModel


class Order(BaseModel):
    id : str
    amount_paid : float
    quantity : int
    product_id : str
    user_id : str
    paid : bool

    class Config:
        orm_mode = True

