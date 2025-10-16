#!/bin/bash
APP_PORT=${PORT:-8080}
cd /app/
# Use Gunicorn from the Docker venv
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm product_order_api.wsgi:application --bind "0.0.0.0:${APP_PORT}"
