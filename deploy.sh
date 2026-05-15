#!/usr/bin/env bash
set -e

export DJANGO_DEBUG="${DJANGO_DEBUG:-False}"
export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS:-enrollsys-enrollsys1.amvera.io,localhost,127.0.0.1}"
export DJANGO_CSRF_TRUSTED_ORIGINS="${DJANGO_CSRF_TRUSTED_ORIGINS:-https://enrollsys-enrollsys1.amvera.io}"
export DJANGO_MEDIA_ROOT="${DJANGO_MEDIA_ROOT:-/data/media}"

export DB_NAME="${DB_NAME:-enrollsys}"
export DB_USER="${DB_USER:-enrollsys}"
export DB_PASSWORD="${DB_PASSWORD:-root}"
export DB_HOST="${DB_HOST:-amvera-enrollsys1-cnpg-enrollsys-db-rw}"
export DB_PORT="${DB_PORT:-5432}"

python manage.py migrate --noinput
python manage.py loaddata core/fixtures/demo_data.json
python manage.py ensure_admin_user
python manage.py collectstatic --noinput

gunicorn app.wsgi:application --bind 0.0.0.0:80 --workers 3 --timeout 120
