from pydantic import BaseModel


class ProductBase(BaseModel):
    asin: str = None
    title: str = None
    description: str = None
    imUrl: str = None
    related: str = None
    salesRank: str = None
    categories: str = None
    brand: str = None
    price: float = None
    #reviews: List[Review] = None

    class Config:
        orm_mode = True


class Product(ProductBase):

    pass


productProperties = ['asin', 'title', 'description', 'imUrl', 'related', 'salesRank', 'categories', 'brand', 'price',
                     'reviews']
