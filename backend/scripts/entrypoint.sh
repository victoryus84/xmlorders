#!/bin/bash
set -e
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
# Start the Django server
exec "$@"