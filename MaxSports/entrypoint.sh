#!/bin/bash

# Exit immediately if any command fails
set -e

# Apply database migrations
echo "👉 Applying database migrations..."
python manage.py migrate

# Collect static files
echo "👉 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "👉 Starting Gunicorn server..."
gunicorn -w 4 MaxSports.wsgi:application -b 0.0.0.0:8000
