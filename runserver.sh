#!/bin/sh

# Run migrations
python manage.py migrate

#Run Tests 
python manage.py test

# Collect static files
python manage.py collectstatic --noinput

# Start the Django app
exec "$@"
