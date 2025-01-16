# syntax=docker/dockerfile:1
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . /app/

# Set execute permissions on the entrypoint script
RUN chmod +x /app/scripts/django/entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput
