import uvicorn
from fastapi import Depends, FastAPI
from repository.database import get_db

from web.ad_controller import ad_router
from web.product_controller import product_router

from fastapi.middleware.cors import CORSMiddleware

from repository.database import initialize_database
from config import products_ip, products_port
app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    product_router,
    tags=["products"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    ad_router,
    tags=["ads"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    initialize_database()
    uvicorn.run(app, host='0.0.0.0', port=products_port)
