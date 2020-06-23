FROM python:3.7
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./configurer-app /configurer
#RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /configurer/requirements.txt
WORKDIR /configurer
RUN pip3 install -r requirements.txt
CMD python ./configurer_main.py

