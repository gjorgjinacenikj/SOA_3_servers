from time import sleep

import consul
from _socket import gethostname
from config import consul_port, consul_ip
client = consul.Consul(host=consul_ip, port=consul_port)
print(client.status.leader())

def discover(app_name):
    index, services = client.health.service(app_name, passing=True)
    for service_info in services:
        service = service_info['Service']
        print(service)

def register(app_port,app_name):
    """
    Registering on consul is straightfoward but we also want the consul server
    to run a health check of our service at given interval.
    This is a fail fast strategy so the interval is low and timeout is not set.
    """
    # create a health check that consul will use to monitor us
    check_http = consul.Check.http('http://{}:{}'.format(gethostname(), app_port),
                                   interval='2s')

    # register on consul with the health check
    while True:
        try:
            service_id = '{}:{}'.format(gethostname(), app_port)
            client.agent.service.register(app_name,
                                          service_id=service_id,
                                          address=gethostname(),
                                          port=app_port,
                                          check=check_http)
            break
        except (ConnectionError, consul.ConsulException) as err:
            print(err)
            print('consul host is down, reconnecting...')
            sleep(0.5)

def deregister(app_name):
    try:
        client.agent.service.deregister(app_name)
    except ConnectionError:
        pass