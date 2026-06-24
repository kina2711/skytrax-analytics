.PHONY: setup build up down logs test clean

setup:
	@echo "Setting up local directories..."
	mkdir -p data/raw data/warehouse

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	@echo "Running tests..."
	python -m pytest tests/

clean:
	docker-compose down -v
	rm -rf __pycache__
	rm -rf .pytest_cache
