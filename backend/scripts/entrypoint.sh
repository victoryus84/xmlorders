#!/bin/bash
set -e

# Wait for PostgreSQL to start
# echo "Waiting for PostgreSQL..."
# while ! curl --silent $PGSQL_HOST:$PGSQL_PORT > /dev/null; do
#   sleep 2
# done
# echo "PostgreSQL started"

# python manage.py clearsessions

# Apply django makemigrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$SUPER_USER"
email = "$SUPER_EMAIL"
password = "$SUPER_PASS"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
EOF

# Collect static files
python manage.py collectstatic --noinput

# Start the Django server
exec "$@"