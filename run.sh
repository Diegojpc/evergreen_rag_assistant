#!/bin/bash

# Export environment variables from .env:
export $(grep -v '^#' .env | xargs)

# Verify if SERVER_HOST environment variable exists
if [ -z "${SERVER_HOST}" ]; then
    echo "Error: SERVER_HOST environment variable is not set"
    exit 1
fi

# Verify if SERVER_PORT environment variable exists
if [ -z "${SERVER_PORT}" ]; then
    echo "Error: SERVER_PORT environment variable is not set"
    exit 1
fi

# Run FastAPI server using uvicorn:
python3 -m uvicorn app.main:app --host ${SERVER_HOST} --port ${SERVER_PORT} --reload
