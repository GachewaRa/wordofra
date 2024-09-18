#!/bin/bash

echo "Applying contenttypes migrations..."
python manage.py migrate contenttypes

echo "Applying accounts migrations..."
python manage.py migrate accounts

echo "Applying auth migrations..."
python manage.py migrate auth

echo "Applying admin migrations..."
python manage.py migrate admin

echo "Creating new blog migrations..."
python manage.py makemigrations blog

echo "Applying blog migrations..."
python manage.py migrate blog

echo "Applying all remaining migrations..."
python manage.py migrate

echo "Showing final migration status..."
python manage.py showmigrations

echo "Migration application complete!"
