#!/bin/bash

echo "Unapplying blog migrations..."
python manage.py migrate blog zero

echo "Removing blog migration files..."
rm -f blog/migrations/0*.py

echo "Applying accounts migrations..."
python manage.py migrate accounts

echo "Recreating and applying blog migrations..."
python manage.py makemigrations blog
python manage.py migrate blog

echo "Applying all remaining migrations..."
python manage.py migrate

echo "Showing migration status..."
python manage.py showmigrations

echo "Migration fix complete!"
