.PHONY: install format lint test build up down clean

install:
	pip install -e .[dev]

format:
	black .
	ruff check --fix .

lint:
	ruff check .
	black --check .

test:
	pytest tests/ -v --asyncio-mode=auto

build:
	docker build -t prism-vortex:latest -f deploy/Dockerfile .

up:
	docker-compose -f deploy/docker-compose.yml up -d --build

down:
	docker-compose -f deploy/docker-compose.yml down

clean:
	rm -rf __pycache__ .pytest_cache *.egg-info build dist
