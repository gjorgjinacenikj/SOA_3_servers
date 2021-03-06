import os
products_ip = os.getenv('products_ip') if os.getenv('products_ip') is not None else '127.0.0.1'
orders_ip = os.getenv('orders_ip') if os.getenv('orders_ip') is not None else '127.0.0.1'
reviews_ip = os.getenv('reviews_ip') if os.getenv('reviews_ip') is not None else '127.0.0.1'
consul_ip = os.getenv('consul_ip') if os.getenv('consul_ip') is not None else '127.0.0.1'

products_port = int(os.getenv('products_port')) if os.getenv('products_port') else 7001
orders_port = int(os.getenv('orders_port')) if os.getenv('orders_port') is not None else 7002
reviews_port = int(os.getenv('reviews_port')) if os.getenv('reviews_port') is not None else 7003
consul_port = int(os.getenv('consul_port')) if os.getenv('consul_port') is not None else 7004

address_format='http://{0}:{1}'

products_add = address_format.format(products_ip, products_port)
orders_add = address_format.format(orders_ip, orders_port)
reviews_add = address_format.format(reviews_ip, reviews_port)
