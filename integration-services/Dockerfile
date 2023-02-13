FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir /django_recipe_api

WORKDIR /django_recipe_api

COPY . .
COPY ./req.txt /req.txt
RUN pip install -r /req.txt
VOLUME /drf_src


CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000