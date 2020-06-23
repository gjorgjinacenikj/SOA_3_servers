import os
from fastapi import Request

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from repository.database import initialize_database
from web.order_controller import order_router
from web.payment_controller import stripe_router
from config import orders_ip, orders_port, consul_port, consul_ip
from starlette_exporter import PrometheusMiddleware, handle_metrics
app = FastAPI()

#static_dir = str(os.path.abspath(os.path.join(__file__, "..")))
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(
    stripe_router,
    tags=["stripe payments"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    order_router,
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

@app.get("/")
def say_hi(request: Request):
    print(request.headers)
    return "Hi. This is server orders. You are {0}".format(request.headers['X-Consumer-Custom-ID'])

if __name__ == "__main__":

    #register(app_port=orders_port, app_name='orders', app_ip = orders_ip)
    initialize_database()
    uvicorn.run("orders_main:app", host='0.0.0.0', port=int(orders_port), reload=True)
    #deregister(app_name='orders')

