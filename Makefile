REGION = us-central1

###### DATA DOWNLOAD AND TRAINING
download-data:
	@echo "Downloading Instacart dataset..."
	uv run python scripts/download_data.py

download-kaggle:
	@echo "Downloading dataset using Kaggle CLI..."
	./scripts/download_kaggle.sh

setup-venv:
	@echo "Setting up Python environment with uv..."
	uv sync

train:
	@echo "Training product recommendation model..."
	cd prod2vec && uv run python prod2vec.py

setup: download-data setup-venv
	@echo "Setup complete!"

train-full: setup train
	@echo "Full training pipeline complete!"

###### DOCKER COMMANDS
up:
	docker-compose up -d

up-prod:
	docker-compose -f docker-compose.prod.yaml up -d

down:
	docker-compose down

down-prod:
	docker-compose -f docker-compose.prod.yaml down

build:
	docker-compose build

build-prod:
	docker-compose -f docker-compose.prod.yaml build

logs:
	docker-compose logs -f

logs-prod:
	docker-compose -f docker-compose.prod.yaml logs -f