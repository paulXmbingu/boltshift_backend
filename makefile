DOCKER_COMPOSE = docker-compose
DOCKERFILE = Dockerfile
DOCKER_NETWORK = my_network


build:
	@$(DOCKER_COMPOSE) build

up:
	@$(DOCKER_COMPOSE) up -d

down:
	@$(DOCKER_COMPOSE) down

restart:
	@$(DOCKER_COMPOSE) restart

clean:
	@$(DOCKER_COMPOSE) down -v

run-web:
	@$(DOCKER_COMPOSE) run --rm backend $(CMD)

shell-web:
	@$(DOCKER_COMPOSE) run --rm backend /bin/bash

test-web:
	@$(DOCKER_COMPOSE) run --rm backend python manage.py test

lint-web:
	@$(DOCKER_COMPOSE) run --rm backend flake8

migrate-web:
	@$(DOCKER_COMPOSE) run --rm backend python manage.py migrate

.PHONY: build up down restart clean run-web shell-web test-web lint-web migrate-web
