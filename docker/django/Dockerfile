# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye AS base

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/opt/poetry/cache \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Копирование файлов Poetry из app/
COPY app/pyproject.toml app/poetry.lock ./

# Development build
FROM base AS development_build

# Установка зависимостей для разработки
RUN poetry install --no-root

# Копирование исходного кода из app/
COPY app/ .

# Создание пользователя для безопасности
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app
USER django

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production build
FROM base AS production_build

# Установка только production зависимостей
RUN poetry install --only=main --no-root

# Копирование исходного кода из app/
COPY app/ .

# Установка проекта
RUN poetry install --only-root

# Создание директории для статических файлов
RUN mkdir -p /var/www/django/static

# Сбор статических файлов
ENV DJANGO_SETTINGS_MODULE=alabuga.settings
ENV DJANGO_SECRET_KEY=build-secret-key
RUN poetry run python manage.py collectstatic --noinput

# Создание пользователя для безопасности
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app /var/www/django
USER django

EXPOSE 8000

# Скрипт запуска для production
COPY docker/django/gunicorn.sh /usr/local/bin/start-web-server
USER root
RUN chmod +x /usr/local/bin/start-web-server
RUN chown django:django /usr/local/bin/start-web-server
USER django

CMD ["/usr/local/bin/start-web-server"]