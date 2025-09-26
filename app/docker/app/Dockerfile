# Указываем образ из https://hub.docker.com/_/python.
FROM python:3.12-slim-bookworm

# Устанавливаем рабочую директорию.
WORKDIR /usr/src/app

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/usr/src/app

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копирование файлов lock и toml (например, poetry.lock и pyproject.toml)
COPY app/pyproject.toml app/poetry.lock ./

# Обновление pip и установка poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Копирование entrypoint.sh
COPY app/docker/app/entrypoint.sh ./entrypoint.sh
COPY app/docker/app/gunicorn.conf ./gunicorn.conf
RUN sed -i 's/\r$//g' entrypoint.sh && chmod +x entrypoint.sh
RUN sed -i 's/\r$//g' gunicorn.conf && chmod +x gunicorn.conf

# Копирование папки app в рабочую директорию.
COPY ../app ./

# Определяем ENTRYPOINT
ENTRYPOINT ["./entrypoint.sh"]