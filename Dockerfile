FROM python:3.6.0b1-alpine
MAINTAINER Roger Simms roger.simms@gmail.com

ENV APP_DIR /src
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

COPY src/requirements.txt $APP_DIR/
RUN pip install -r requirements.txt
