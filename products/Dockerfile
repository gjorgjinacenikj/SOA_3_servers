FROM python:3.7
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./products-app /products
#RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /products/requirements.txt
WORKDIR /products
RUN pip3 install -r requirements.txt
CMD python ./products_main.py

