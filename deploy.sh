#!/bin/bash
# Railway deployment script

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn zamreach.wsgi --bind 0.0.0.0:$PORT --workers 3
