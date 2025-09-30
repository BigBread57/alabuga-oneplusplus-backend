#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Применение миграций
echo "Applying database migrations..."
poetry run python manage.py migrate --noinput

# Сбор статических файлов
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Создание суперпользователя, если необходимо
if [ "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "Creating superuser..."
    poetry run python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
email = '${DJANGO_SUPERUSER_EMAIL}'
password = '${DJANGO_SUPERUSER_PASSWORD}'
if not User.objects.filter(email=email).exists():
    user = User.objects.create_superuser(
        username=email,
        email=email,
        password=password
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
"
fi

# Запуск Gunicorn
echo "Starting Gunicorn..."
exec poetry run gunicorn alabuga.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
