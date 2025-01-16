#!/bin/bash

# Wait for PostgreSQL to be ready
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Apply django makemigrations
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$DJANGO_USER"
email = "$DJANGO_EMAIL"
password = "$DJANGO_PASS"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
EOF

# Start the Django server
exec "$@"