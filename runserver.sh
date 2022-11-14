#!/bin/bash

docker network create docker_network
docker-compose stop
docker-compose build
docker-compose up --detach
docker-compose stop
docker-compose run --rm api alembic revision --autogenerate
docker-compose run --rm api alembic upgrade head
docker-compose up --detach
docker-compose logs --follow --tail 100
