#!/bin/bash

set -e

PROJECT_ROOT="."

mkdir -p "$PROJECT_ROOT/app/services"
mkdir -p "$PROJECT_ROOT/app/rules"
mkdir -p "$PROJECT_ROOT/app/templates"
mkdir -p "$PROJECT_ROOT/app/static"

touch "$PROJECT_ROOT/app/__init__.py"
touch "$PROJECT_ROOT/app/models.py"
touch "$PROJECT_ROOT/app/routes.py"

touch "$PROJECT_ROOT/app/services/cart_service.py"
touch "$PROJECT_ROOT/app/services/pricing_service.py"

touch "$PROJECT_ROOT/app/rules/engine.py"
touch "$PROJECT_ROOT/app/rules/base.py"
touch "$PROJECT_ROOT/app/rules/promotions.py"

touch "$PROJECT_ROOT/app/templates/base.html"
touch "$PROJECT_ROOT/app/templates/products.html"
touch "$PROJECT_ROOT/app/templates/cart.html"
touch "$PROJECT_ROOT/app/templates/summary.html"

touch "$PROJECT_ROOT/app/static/styles.css"

touch "$PROJECT_ROOT/config.py"
touch "$PROJECT_ROOT/run.py"
touch "$PROJECT_ROOT/requirements.txt"
touch "$PROJECT_ROOT/README.md"

echo "Struktura została utworzona."

