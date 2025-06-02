#!/bin/bash

# Usage: ./deploy.sh [devl|stag|prod]

set -e

ENV=$1

if [[ "$ENV" != "devl" && "$ENV" != "stag" && "$ENV" != "prod" ]]; then
  echo "Error: Argument must be one of: devl, stag, prod" >&2
  exit 1
fi

ENV_FILE=".env.$ENV"
COMPOSE_FILE="docker-compose.$ENV.yml"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: $ENV_FILE does not exist." >&2
  exit 2
fi

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Error: $COMPOSE_FILE does not exist." >&2
  exit 3
fi

# Copy .env.$ENV to .env in root, backend, and frontend
cp "$ENV_FILE" .env
cp "$ENV_FILE" backend/.env
cp "$ENV_FILE" frontend/.env

echo "Copied $ENV_FILE to .env, backend/.env, and frontend/.env."

docker compose -f "$COMPOSE_FILE" -p "aiph-zeta-$ENV" up -d --build

if [[ "$ENV" == "devl" ]]; then
  cd backend
  echo "Waiting 5 seconds for services to be ready..."
  sleep 5
  alembic upgrade head
  uvicorn app.main:app --reload
  cd ..
  docker compose -f "$COMPOSE_FILE" -p "aiph-zeta-$ENV" down
fi



