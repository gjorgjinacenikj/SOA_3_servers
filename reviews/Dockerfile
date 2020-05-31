FROM python:3.7
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./reviews-app /reviews
#RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /reviews/requirements.txt
WORKDIR /reviews
RUN pip3 install -r requirements.txt
CMD python ./reviews_main.py

