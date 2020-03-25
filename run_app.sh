#!/bin/bash

source venv/bin/activate

export APP_ENV=prd
export FLASK_APP=application.py

echo "Launch API"
uvicorn api:api --reload &

echo "Launch Flask Client"
flask run &
