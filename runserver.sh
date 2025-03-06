#!/bin/sh

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django app
exec "$@"
