.PHONY: setup install dev test lint format migrate rollback db-seed clean help run shell docs build deploy

# Variables
PYTHON = python
PIP = pip
VENV = venv
APP_NAME = fastapi-laravel
ALEMBIC = alembic
UVICORN = uvicorn
PYTEST = pytest
PYTEST_ARGS = -v
FLAKE8 = flake8
BLACK = black
ISORT = isort
PYDOC = pydoc-markdown
PORT = 8000
HOST = 0.0.0.0
APP_MODULE = app.main:app

# Default target
.DEFAULT_GOAL := help

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==================================================================================== #
# DEVELOPMENT
# ==================================================================================== #

setup: ## Set up the development environment
	$(PYTHON) -m venv $(VENV)
	$(MAKE) install
	@echo "Creating necessary directories..."
	mkdir -p app/config app/controllers app/views app/models app/services
	mkdir -p app/repositories app/middleware app/exceptions app/utils
	mkdir -p migrations app/static app/templates tests
	mkdir -p app/storage/uploads app/storage/logs
	touch .env
	@echo "Setup complete! Run 'make install' to install dependencies."

install: ## Install dependencies
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

dev: ## Run development server with auto-reload
	$(UVICORN) $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

run: ## Run production server
	$(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT)

shell: ## Run Python shell with app context
	$(PYTHON) -c "import sys; sys.path.insert(0, '.'); from app.models.base import Base; from app.models.user import User; from app.utils.database import SessionLocal; db = SessionLocal(); print('App shell initialized. Variables available: db, Base, User')"

# ==================================================================================== #
# DATABASE
# ==================================================================================== #

migrate: ## Generate a new migration
	@read -p "Enter migration name: " name; \
	$(ALEMBIC) revision --autogenerate -m "$$name"

migrate-up: ## Run all migrations
	$(ALEMBIC) upgrade head

migrate-down: ## Rollback the latest migration
	$(ALEMBIC) downgrade -1

db-seed: ## Seed the database with initial data
	$(PYTHON) -m app.cli.seed

db-reset: ## Reset the database (drop and recreate)
	$(ALEMBIC) downgrade base
	$(ALEMBIC) upgrade head

# ==================================================================================== #
# TESTING & LINTING
# ==================================================================================== #

test: ## Run tests
	$(PYTEST) $(PYTEST_ARGS)

test-cov: ## Run tests with coverage
	$(PYTEST) --cov=app tests/ --cov-report=term --cov-report=html

lint: ## Run linting
	$(FLAKE8) app/ tests/

format: ## Format code with Black and isort
	$(BLACK) app/ tests/
	$(ISORT) app/ tests/

# ==================================================================================== #
# SCAFFOLDING
# ==================================================================================== #

make-controller: ## Create a new controller
	@read -p "Enter controller name: " name; \
	$(PYTHON) manage.py make_controller $$name

make-model: ## Create a new model
	@read -p "Enter model name: " name; \
	$(PYTHON) manage.py make_model $$name

make-service: ## Create a new service
	@read -p "Enter service name: " name; \
	$(PYTHON) manage.py make_service $$name

make-repository: ## Create a new repository
	@read -p "Enter repository name: " name; \
	$(PYTHON) manage.py make_repository $$name

# ==================================================================================== #
# DOCUMENTATION
# ==================================================================================== #

docs: ## Generate API documentation
	$(PYDOC) -I app -O docs

# ==================================================================================== #
# DEPLOYMENT
# ==================================================================================== #

requirements: ## Generate requirements.txt file
	$(PIP) freeze > requirements.txt

build: ## Build the application for production
	@echo "Building application for production..."
	$(PIP) install -r requirements.txt
	$(MAKE) migrate-up

deploy: ## Deploy the application (placeholder)
	@echo "Deploying application..."
	$(MAKE) build
	$(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT) --workers 4

# ==================================================================================== #
# MAINTENANCE
# ==================================================================================== #

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf */*/*/__pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	@echo "Cleaned!"

deep-clean: clean ## Clean up virtual environment as well
	rm -rf $(VENV)
	@echo "Virtual environment removed!"