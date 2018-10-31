FROM python:3.7

ENV PYTHONUNBUFFERED 1
ARG ENV=dev

RUN mkdir /app
WORKDIR /app
ADD ./requirements /app/requirements
RUN pip install -Ur requirements/$ENV.txt
ADD . /app/
