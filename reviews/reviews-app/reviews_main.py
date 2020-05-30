import uvicorn
from fastapi import Depends, FastAPI
from repository.database import get_db
from web.review_controller import review_router
from fastapi.middleware.cors import CORSMiddleware
from config import reviews_ip, reviews_port
from repository.database import initialize_database

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
    review_router,
    tags=["reviews"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    initialize_database()
    uvicorn.run(app, host=reviews_ip, port=reviews_port)
