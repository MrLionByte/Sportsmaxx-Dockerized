#!/bin/bash

# Exit immediately if any command fails
set -e

echo "👉 Applying database migrations..."
# python manage.py migrate

echo "👉 Collecting static files..."
# python manage.py collectstatic --noinput

echo "👉 Starting Gunicorn server..."
gunicorn -w 4 MaxSports.wsgi:application -b 0.0.0.0:8000
