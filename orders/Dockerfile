FROM python:3.7
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./orders-app /orders
#RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /orders/requirements.txt
WORKDIR /orders
RUN pip3 install -r requirements.txt
CMD python ./orders_main.py

