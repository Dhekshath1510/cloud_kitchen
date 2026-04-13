#!/bin/bash
# Azure App Service startup script for FastAPI

# Azure provides the PORT environment variable natively
echo "Starting Application on port $PORT"

# Run migrations if necessary before start
# alembic upgrade head

# Execution strategy tailored for high-scale environments using Uvicorn workers on Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT
