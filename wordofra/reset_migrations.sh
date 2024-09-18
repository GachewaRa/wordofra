#!/bin/bash

# Backup the database
echo "Backing up the database..."
sudo -u postgres pg_dump my_portfolio_db > backup.sql

# Reset migration history
echo "Resetting migration history..."
sudo -u postgres psql my_portfolio_db << EOF
DELETE FROM django_migrations WHERE app IN ('admin', 'auth', 'accounts', 'contenttypes');
\q
EOF

# Remove old migration files
echo "Removing old migration files..."
rm -f accounts/migrations/0*.py

# Make and apply migrations
echo "Making and applying migrations..."
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

echo "Migration reset complete!"
