# 🚀 Production Deployment Guide

Руководство по развертыванию в production окружении.

## Предварительные требования

- Docker & Docker Compose
- Nginx Proxy с Let's Encrypt (или любой reverse proxy)
- Домен с настроенными DNS записями

## Быстрый деплой

### 1. Подготовка сервера

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd alabuga-oneplusplus-backend

# Создайте .env файл из примера
cp .env.production.example .env
```

### 2. Настройка переменных окружения

Отредактируйте `.env`:

```bash
# Обязательно измените:
DJANGO_SECRET_KEY=your-random-secret-key-here  # Генерируйте через: openssl rand -base64 50
POSTGRES_PASSWORD=your-strong-password-here
DJANGO_DATABASE_PASSWORD=your-strong-password-here
DJANGO_SUPERUSER_PASSWORD=your-admin-password-here
DOMAIN_NAME=your-domain.com
DJANGO_SUPERUSER_EMAIL=admin@your-domain.com
```

### 3. Запуск

```bash
docker-compose -f docker-compose.production.yml up -d
```

### 4. Проверка

```bash
# Проверить статус сервисов
docker-compose -f docker-compose.production.yml ps

# Посмотреть логи
docker-compose -f docker-compose.production.yml logs -f backend
```

---

## Архитектура Production

```
Internet
   │
   ▼
[nginx-proxy + Let's Encrypt]
   │
   ├─► Nginx (:80)
   │     │
   │     ├─► Backend (:8000) - Django + Gunicorn
   │     └─► Frontend (:8080) - Next.js
   │
   ├─► PostgreSQL (:5432)
   ├─► Redis (:6379)
   ├─► Celery Worker
   └─► Celery Beat
```

---

## Настройка Nginx Proxy

Если используете [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy):

```yaml
# Уже настроено в docker-compose.production.yml
environment:
  VIRTUAL_HOST: your-domain.com
  VIRTUAL_PORT: 80
  LETSENCRYPT_HOST: your-domain.com
```

Nginx автоматически:
- Получит SSL сертификат от Let's Encrypt
- Настроит reverse proxy
- Настроит автоматическое обновление сертификатов

---

## Обновление приложения

### Стандартное обновление

```bash
# Скачать новые образы
docker-compose -f docker-compose.production.yml pull

# Пересоздать контейнеры
docker-compose -f docker-compose.production.yml up -d

# Применить миграции (если нужно)
docker-compose -f docker-compose.production.yml exec backend poetry run python manage.py migrate
```

### Zero-downtime обновление

```bash
# Скачать новые образы
docker-compose -f docker-compose.production.yml pull backend celery-worker celery-beat

# Обновить Celery
docker-compose -f docker-compose.production.yml up -d celery-worker celery-beat

# Обновить Backend с масштабированием
docker-compose -f docker-compose.production.yml up -d --no-deps --scale backend=2 backend
sleep 10
docker-compose -f docker-compose.production.yml up -d --no-deps --scale backend=1 backend
```

---

## Резервное копирование

### База данных

```bash
# Создать backup
docker-compose -f docker-compose.production.yml exec postgres pg_dump -U postgres alabuga_db > backup_$(date +%Y%m%d).sql

# Восстановить backup
docker-compose -f docker-compose.production.yml exec -T postgres psql -U postgres alabuga_db < backup_20240101.sql
```

### Медиа файлы

```bash
# Создать архив медиа
docker run --rm -v $(pwd)/django_media:/data -v $(pwd):/backup alpine tar czf /backup/media_backup_$(date +%Y%m%d).tar.gz -C /data .

# Восстановить медиа
docker run --rm -v $(pwd)/django_media:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup_20240101.tar.gz -C /data
```

---

## Мониторинг

### Логи

```bash
# Все сервисы
docker-compose -f docker-compose.production.yml logs -f

# Только backend
docker-compose -f docker-compose.production.yml logs -f backend

# Последние 100 строк
docker-compose -f docker-compose.production.yml logs --tail=100 backend
```

### Статус сервисов

```bash
# Проверить работающие контейнеры
docker-compose -f docker-compose.production.yml ps

# Проверить использование ресурсов
docker stats
```

### Celery мониторинг

В production рекомендуется использовать внешний мониторинг:
- Flower (уже включен, но требует настройки безопасности)
- Prometheus + Grafana
- Sentry для ошибок

---

## Дополнительные настройки

### Автоматические backup'ы

Создайте cron job:

```bash
# /etc/cron.d/alabuga-backup
0 2 * * * root cd /path/to/project && docker-compose -f docker-compose.production.yml exec postgres pg_dump -U postgres alabuga_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Настройка Sentry

Добавьте в `.env`:

```bash
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### Настройка email

Добавьте в `.env`:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---
