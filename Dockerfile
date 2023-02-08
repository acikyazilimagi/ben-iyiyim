FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install git tini build-essential libpq-dev gcc -y

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./start-django.sh /start-django
RUN chmod +x /start-django

ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/start-django"]