import os

import consul
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from repository.database import initialize_database
from web.order_controller import order_router
from web.payment_controller import stripe_router
from config import orders_ip, orders_port, consul_port, consul_ip
from service_registry import register, deregister
app = FastAPI()

#static_dir = str(os.path.abspath(os.path.join(__file__, "..")))
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
# register_to_consul()

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

if __name__ == "__main__":

    cons = consul.Consul(host=consul_ip, port=consul_port)


    register(app_port=orders_port, app_name='orders')
    initialize_database()
    uvicorn.run("orders_main:app", host='0.0.0.0', port=int(orders_port), reload=True)
    deregister(app_name='orders')

