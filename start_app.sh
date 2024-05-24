#!/bin/bash

echo "Prepping Django App..."
python manage.py makemigrations dummy  # Create migrations for the dummy app
python manage.py migrate  # Apply migrations to the database
echo

echo "Creating Superuser..."
DJANGO_SUPERUSER_PASSWORD="$DJANGO_SUPERUSER_PASSWORD" \
python manage.py createsuperuser --noinput --username=admin --email=test@test.com
echo

echo "Starting Django App..."
python manage.py runserver 0.0.0.0:8000
