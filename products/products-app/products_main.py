import uvicorn
from fastapi import Depends, FastAPI
from repository.database import get_db
from fastapi import Request

from web.product_controller import product_router

from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from repository.database import initialize_database
from config import products_ip, products_port




app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:9090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(
    product_router,
    tags=["products"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@app.get("/")
def say_hi(request: Request):
    print(request.headers)
    return "Hi. This is server products. You are {0}".format(request.headers['X-Consumer-Custom-ID'])


if __name__ == "__main__":
    initialize_database()
    uvicorn.run(app, host='0.0.0.0', port=products_port)
