# Proxy Service

Сервис прокси-доступа с регистрацией, личным кабинетом, Celery-рассылкой ключей и desktop-клиентом.

## Что реализовано

- `FastAPI + SQLAlchemy + PostgreSQL`
- `Celery + Redis` для отправки ключей по email
- `Vue 3 + Vuetify` для web-интерфейса
- `Electron + Vue desktop client` для подключения по ключу
- `WebSocket /ws/status` для статуса подключения в реальном времени
- `Swagger` доступен по `http://localhost:8000/docs`

## Сервисы

- `frontend` — SPA на `http://localhost`
- `backend` — API на `http://localhost:8000`
- `postgres` — PostgreSQL
- `redis` — брокер Celery
- `celery_worker` — фоновые email-задачи
- `flower` — мониторинг Celery на `http://localhost:5555`

## Запуск проекта

```bash
docker compose up -d --build
```

После старта будут автоматически созданы тестовые виртуалки:

- `proxy-1` → `127.0.0.1:1080 (socks5)`
- `proxy-2` → `127.0.0.1:8080 (http)`
- `proxy-3` → `127.0.0.1:3128 (https)`

## Переменные окружения

Файл-шаблон: `.env.example`

Если захотите запускать backend локально без Docker, скопируйте шаблон в `backend/.env` и при необходимости подставьте свои значения.

Для демо по умолчанию используется:

- `EMAIL_BACKEND=console`

В этом режиме Celery worker печатает письмо с ключом в свои логи. Это удобно для локальной проверки без реального SMTP.

Если нужны настоящие письма, переключите:

```env
EMAIL_BACKEND=smtp
SMTP_HOST=...
SMTP_PORT=...
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM_EMAIL=...
SMTP_USE_TLS=true
```

## Как проверить web-часть

1. Откройте `http://localhost/register`
2. Зарегистрируйтесь
3. Проверьте логи `celery_worker` и скопируйте ключ активации
4. Войдите через `http://localhost/login`
5. Откройте `http://localhost/profile`
6. Посмотрите текущий ключ, обновите его при необходимости и смените пароль

## Как получить ключ

- После регистрации backend ставит Celery-задачу
- Celery worker отправляет письмо
- В `console`-режиме письмо выводится в логах воркера
- В `smtp`-режиме письмо уходит через настроенный SMTP-сервер

## Desktop-приложение

Файлы лежат в `desktop-client/`.

Установка зависимостей:

```bash
cd desktop-client
npm install
```

Запуск в dev-режиме:

```bash
npm run dev
```

Запуск Electron из собранного renderer:

```bash
npm run start
```

Что делает desktop-клиент:

1. Принимает `backend URL` и `activation key`
2. Отправляет ключ на `POST /api/activate-key`
3. Получает свободную виртуалку и desktop token
4. Подключается к `WebSocket /ws/status?token=...`
5. Показывает статусы `waiting`, `connected`, `disconnected`, `error`, `no_free_vms`
6. По кнопке `Disconnect` освобождает виртуалку через `POST /api/disconnect`

Если backend запущен через `docker compose`, оставьте `http://localhost:8000` в поле `Backend URL`.

## Основные API

- `POST /api/register`
- `POST /api/login`
- `GET /api/profile`
- `POST /api/refresh-key`
- `POST /api/change-password`
- `POST /api/activate-key`
- `POST /api/disconnect`
- `GET /health`
- `WS /ws/status?token=...`
- `WS /ws/connection-status/{user_id}?token=...`

## Тесты

Установка dev-зависимостей:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Запуск:

```bash
pytest tests -q
```

## Примечания

- Ключ активации одноразовый и удаляется после первого успешного подключения.
- Если свободных виртуалок нет, API вернет `503`.
- Для локального запуска миграции не используются: таблицы создаются автоматически при старте приложения.
