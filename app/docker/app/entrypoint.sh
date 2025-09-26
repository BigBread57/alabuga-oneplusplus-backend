#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

# Выполняем миграции и сбор статики только для app-сервиса
if [ "$SERVICE_TYPE" = "app" ]; then
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py delete_webhook
    python manage.py set_webhook
    gunicorn roblox_trade.asgi:application --config gunicorn.conf
fi

exec "$@"