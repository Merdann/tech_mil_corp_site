FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /api/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /api/requirements.txt

COPY ./ /api
WORKDIR /api
