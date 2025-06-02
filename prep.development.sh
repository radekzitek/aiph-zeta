#!/bin/bash

# Paths to backend and frontend directories
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"
ENV_SOURCE=".env.development"

# Copy .env.development to backend as .env
cp "$ENV_SOURCE" "$BACKEND_DIR/.env"

# Copy .env.development to frontend as .env
cp "$ENV_SOURCE" "$FRONTEND_DIR/.env"

echo ".env.development copied to backend and frontend as .env"