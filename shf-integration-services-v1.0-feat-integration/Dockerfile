FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir /django_recipe_api

WORKDIR /django_recipe_api

COPY . .
COPY ./req.txt /req.txt
RUN pip install -r /req.txt
VOLUME /drf_src


RUN chmod +x migrations-entrypoint.sh
ENTRYPOINT ["./migrations-entrypoint.sh"]