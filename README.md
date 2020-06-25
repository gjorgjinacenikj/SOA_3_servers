Gjorgjina Cenikj's (id: 161517) student project for the 'Service Oriented Architectures' course @ Faculty Of Computer Science and Engineering
##PROJECT SETUP:
- Run 'docker-compose up --build' in the root directory
- Wait until Kong is running properly. Then, execute a GET request to 'http://localhost:7000' to configure Kong's services and authentication. You could also do this manually using Konga's GUI.

##SERVICE CONFIGURATION:
- port 8000 - Kong proxy (credentials for basic authentication - username:'user1', password: 'password')
    - 'localhost:8000/products_service' - base url of products service accessed through Kong
    - 'localhost:8000/orders_service' - base url of orders service accessed through Kong
    - 'localhost:8000/reviews_service' - base url of reviews service accessed through Kong
- port 8001 - Kong admin
- port 1337 - Konga (might need some time to stabilize)
- port 7000 - Configurer service
- port 8500 - Consul
- port 9090 - Prometheus
- port 3000 - Grafana (credentials - username:'admin', password: 'admin')
- port 9200 - Elastic search
- port 5601 - Kibana (might need some time to stabilize)

##PROJECT DETAILS:
#### Main services
This project contains 3 main services: products, orders, and reviews, all of which are FastAPI apps, and use a separate postgres database.
- The **products service** provides information about products and does not depend on any of the two other services. 
    - Relevant endpoints:
        - GET /products/{id} - returns the product data for the product with the specified id
        - GET /products - returns max 100 products
- The **orders service** enables users to order and pay for products using a credit card. It depends on the product service, from which it gets the price for each product, in order to calculate the total order sum. 
    - Relevant endpoints:
        - GET /orders - returns max 100 orders
        - GET /order?user_id&product_id - returns a boolean indicator of whether the user has bought the product
        - GET /create-order?product_id&quantity - creates a new order for the logged in user and returns the payment page. The payment process is implemented using Stripe and one of the following credit card details can be used for testing:
            - Credit card number: 4242424242424242
            - CVC: any 3 digits
            - Validity date: Any future date
            - Other options can be found on Stripe's testing page documentation: https://stripe.com/docs/testing
- The **reviews service** enables users to leave a review for a product. This service depends on the orders service, to which it sends a call to check whether the user has previously bought the product, i.e. to check if they are allowed to write a review for it
    - Relevant endpoints:
        - GET /reviews - returns max 100 reviews
        - GET /reviews?product_id - returns all reviews for a product
        - POST /reviews - creates a new review for the product if the user has previously bought it
            - Expected request body: {product_id: string, overall: float, reviewText: string}
        
#### Utility services
- **Service discovery and registry**      
    - **Consul** - Runs on port 8500. Provides service health check, discovery, configuration, and segmentation. 
    - **Registrator** - Automatically registers and unregisters services by inspecting containers as they come online. It supports pluggable service registries, which currently includes Consul, etcd and SkyDNS.
- **Logging and monitoring**
    - **Filebeat** - In an ELK-based logging pipeline, Filebeat plays the role of the logging agent. It is installed on the machine generating the log files, tailing them, and forwarding the data to either Logstash for more advanced processing or directly into Elasticsearch for indexing. In our case, it sends the data to Elasticsearch directly.
    - **Elasticsearch** - Runs on port 9200. Elasticsearch is where the indexing, search, and analysis magic happens. It supports structured or unstructured text, numerical data, or geospatial data. In our case, it is used to store the logs from Filebeat and access them through Kibana.
    - **Kibana** - Runs on port 5601. A visualization layer that works on top of Elasticsearch, providing users with the ability to manage the Elastic stack, and analyze and visualize the data. After a successful setup, a Filebeat index is configured for Elasticsearch. An index pattern can be defined for it and visualizations can be made from its logs.
    - **Prometheus** - Runs on port 9090. It is a monitoring and alerting tool that scrapes metrics from instrumented jobs and uses it to either aggregate and record new time series from existing data or generate alerts. Grafana or other API consumers can be used to visualize the collected data. We use the PrometheusMiddleware in the FastAPI apps to expose a '/metrics' endpoint from which Prometheus collects health data from each of the services and sends it to Grafana.
    - **Grafana** - Runs on port 3000. We use it to visualize the metrics from Prometheus. Once started, you have to login (username: 'admin', password, 'admin'). Prometheus is already configured, you can find it under 'datasources' and import any of the dashboards it provides.
- **API Gateway**
    - **Kong** - Runs on ports 8000 and 8001. It is an API Gateway that provides load balancing, logging, authentication, rate-limiting, transformations, and other functions through various plugins. We use it for routing and basic authentication of the 3 services.
    - **Konga** - Runs on port 1337. A GUI for managing Kong. It can be used to setup the services, routes, consumers and authentication instead of using the Configurer endpoint.
    - **Configurer** - Runs on port 7000. A FastAPI app whose sole purpose is to setup kong. It contains a single endpoint accessible at 'http://localhost:7000', which executes calls to Kong, to configure the following things:
        - add products, orders, and reviews as services named 'products_service', 'orders_service', and 'reviews_service', correspondingly
        - add a route for each of the services, where each route is obtained by appending the service name to Kong's proxy url
        - add a consumer with custom_id=user1 and username=user1
        - add the basic authentication plugin to all services
        - add credentials for the consumer: username='user1', password='password'
- **Circuit breakers**
    - **Pybreaker** - not a docker service, but implemented for protecting methods in each of the 3 main services
            