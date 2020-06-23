import os
import time

import requests
import uvicorn
from fastapi import Depends, FastAPI
from fastapi import Request

from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import products_ip, products_port, products_add, orders_add, reviews_add




app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:9090",
]

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

@app.get("/")
def say_hi(request: Request):
    kong_port=os.getenv('kong_port')
    kong_ip=os.getenv('kong_ip')
    kong_url='http://{0}:{1}'.format(kong_ip,kong_port)
    kong_services_url=kong_url+'/services'
    kong_consumers_url=kong_url+'/consumers'
    kong_plugins_url=kong_url+'/plugins'
    requests.post(kong_consumers_url, {'custom_id':'user1', 'username':'user1'})
    service_kong_configuration = [
        {'name': 'orders_service', 'url': orders_add},
        {'name': 'products_service', 'url': products_add},
        {'name': 'reviews_service', 'url': reviews_add},
    ]
    for service_config in service_kong_configuration:
        requests.post(kong_services_url, service_config)
    time.sleep(3)
    for service_config in service_kong_configuration:
        route_config={'paths': [service_config['name']], 'methods': ['GET', 'POST']}
        kong_routes_url='{0}/{1}/routes'.format(kong_services_url, service_config['name'])
        requests.post(kong_routes_url, route_config)
    requests.post(kong_plugins_url, {'name':'basic-auth'})
    requests.post(kong_consumers_url+'user1/basic-auth', {'username':'user1', 'password':'password'})

    return "Kong configured"


if __name__ == "__main__":

    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('configurer_port')) )
