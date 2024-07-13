#!/usr/bin/env bash

export NICEGUI_STORAGE_PATH="/tmp"


if [ "$1" = "prod" ]; then
    echo "Starting Uvicorn server in production mode..."
    # we also use a single worker in production mode so socket.io connections are always handled by the same worker
    uvicorn main:app --workers 1 --log-level info --port "8080" --host "0.0.0.0"
elif [ "$1" = "dev" ]; then
    echo "Starting Uvicorn server in development mode..."
    # reload implies workers = 1
    uvicorn main:app --reload --log-level debug --port "8080" --host "0.0.0.0"
else
    echo "Invalid parameter. Use 'prod' or 'dev'."
    exit 1
fi