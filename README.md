# Indoors Test Task — Cat Breeders Service

Тестовое задание для компании **Indoors Navigation**.

Проект представляет собой сервис для заводчиков котов. Пользователь может зарегистрироваться, войти по JWT, управлять своими котами, отправлять сообщения другим пользователям через WebSocket и просматривать историю сообщений через REST API.

## Стек

Backend:

- Python 3.12
- Django 6
- Django REST Framework
- Simple JWT
- Django Channels
- Daphne
- PostgreSQL
- Redis
- pytest
- uv

Frontend:

- Angular
- TypeScript
- HTML/CSS

Infrastructure:

- Docker
- Docker Compose

## Что Реализовано

Пользователи:

- регистрация пользователя;
- JWT-авторизация;
- получение access/refresh токенов.

Коты:

- создание кота;
- получение списка своих котов;
- редактирование своего кота;
- удаление своего кота;
- ограничение доступа по владельцу;
- валидация поля `fluffiness` от 1 до 10.

Сообщения:

- WebSocket-подключение с JWT-аутентификацией;
- отправка сообщений другим пользователям;
- сохранение сообщений в базе данных;
- получение истории сообщений через REST API;
- валидация WebSocket-сообщений.

Frontend:

- страница регистрации;
- страница входа;
- управление котами;
- страница сообщений;
- отправка сообщений через WebSocket;
- отображение истории сообщений.

## Структура

```text
indoors-test-task/
├── backend/
│   ├── api/
│   ├── cats/
│   ├── chat/
│   ├── config/
│   ├── users/
│   ├── Dockerfile
│   └── manage.py
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── angular.json
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

## Быстрый Запуск Через Docker

Скопировать переменные окружения:

```bash
cp .env.example .env
```

Собрать и запустить контейнеры:

```bash
docker compose up -d --build
```

Применить миграции:

```bash
docker compose exec backend uv run python manage.py migrate
```

Собрать статику внутри контейнера:

```bash
 docker compose exec backend uv run python manage.py collectstatic --noinput
```

Создай суперпользователя внутри backend-контейнера:

```bash
docker compose exec backend uv run python manage.py createsuperuser
```

Пример для создания суперпользователя:
```
Username: admin
Email address: admin@example.com
Password: Admin12345!
Password (again): Admin12345!
```

Приложение будет доступно по адресам:

```text
Frontend:    http://localhost:4200

Backend API: http://localhost:8000/api/v1/ - Сам base URL возвращает 404, так как отдельный endpoint для /api/v1/ не реализован. 

Django admin: http://localhost:8000/admin/
```

После первого запуска миграции обязательны. Без них регистрация упадёт, потому что в PostgreSQL ещё не будет стандартных таблиц Django, например `auth_user`.

## Frontend Маршруты

```text
http://localhost:4200/register
http://localhost:4200/login
http://localhost:4200/cats
http://localhost:4200/messages
```

## REST API

Auth:

```text
POST /api/v1/auth/register/
POST /api/v1/auth/token/
POST /api/v1/auth/token/refresh/
```

Cats:

```text
GET    /api/v1/cats/
POST   /api/v1/cats/
GET    /api/v1/cats/{id}/
PATCH  /api/v1/cats/{id}/
DELETE /api/v1/cats/{id}/
```

Messages:

```text
GET /api/v1/messages/
```

## Проверка Через Frontend

1. Открыть регистрацию:

```text
http://localhost:4200/register
```

2. Создать пользователя, например:

```text
username: name
password: testpassword123
```

3. Войти:

```text
http://localhost:4200/login
```

После входа пользователь будет перенаправлен на страницу котов.

4. Открыть страницу котов:

```text
http://localhost:4200/cats
```

На странице можно создать, отредактировать, удалить кота и увидеть список только своих котов.

5. Открыть страницу сообщений:

```text
http://localhost:4200/messages
```

Для отправки сообщения нужно указать ID получателя и текст сообщения.

## Проверка REST API Через curl

Регистрация:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "name", "password": "testpassword123"}'
```

Получение JWT:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "name", "password": "testpassword123"}'
```

Ответ содержит `refresh` и `access`:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Создание кота:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/cats/ \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Barsik",
    "age": 2,
    "breed": "Siberian",
    "fluffiness": 8
  }'
```

Получение списка котов:

```bash
curl http://127.0.0.1:8000/api/v1/cats/ \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## WebSocket

WebSocket endpoint:

```text
ws://127.0.0.1:8000/ws/chat/?token=ACCESS_TOKEN
```

Формат отправки сообщения:

```json
{
  "receiver_id": 2,
  "text": "Привет!"
}
```

Пример успешного ответа отправителю:

```json
{
  "status": "sent",
  "message": {
    "id": 1,
    "sender_id": 1,
    "sender_username": "name",
    "receiver_id": 2,
    "text": "Привет!",
    "created_at": "2026-05-18T10:00:00Z"
  }
}
```

Сценарий проверки:

1. Зарегистрировать двух пользователей.
2. Получить JWT access token для каждого пользователя.
3. Открыть два WebSocket-подключения, например через Postman.
4. Первое подключение открыть с токеном пользователя 1.
5. Второе подключение открыть с токеном пользователя 2.
6. Из WebSocket пользователя 1 отправить сообщение с `receiver_id` пользователя 2.
7. Пользователь 2 получит сообщение в реальном времени.

Сообщение также сохранится в базе данных и будет доступно через:

```text
GET /api/v1/messages/
```

## Как Узнать ID Пользователей

Через Django shell:

```bash
docker compose exec backend uv run python manage.py shell
```

```python
from django.contrib.auth import get_user_model

User = get_user_model()

for user in User.objects.all():
    print(user.id, user.username)
```

## Тесты

Локально:

```bash
uv run pytest -q
```

Внутри backend-контейнера:

```bash
docker compose exec backend uv run pytest -q
```

Тестами покрыты:

- регистрация пользователя;
- получение JWT;
- CRUD котов;
- права доступа к котам;
- валидация котов;
- сервис создания сообщений;
- история сообщений.

## Локальный Запуск Без Docker

Установить зависимости:

```bash
uv sync
```

Применить миграции:

```bash
uv run python backend/manage.py migrate
```

Запустить backend через Daphne:

```bash
cd backend
uv run daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

Для локальной проверки WebSocket нужен Redis. Его можно запустить отдельно:

```bash
docker compose up -d redis
```

Запустить frontend:

```bash
cd frontend
npm install
npm start
```

При локальном запуске backend вне Docker обычно используются:

```env
DB_HOST=localhost
REDIS_HOST=localhost
```

При запуске backend внутри Docker Compose используются имена сервисов:

```env
DB_HOST=postgres
REDIS_HOST=redis
```

## Переменные Окружения

Пример находится в `.env.example`.

Основные переменные:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=postgres
POSTGRES_DB=indoors_db
POSTGRES_USER=indoors_user
POSTGRES_PASSWORD=change-me
DB_HOST=postgres
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:4200
CSRF_TRUSTED_ORIGINS=http://localhost:4200

REDIS_HOST=redis
REDIS_PORT=6379

BACKEND_PORT=8000
FRONTEND_PORT=4200
```

## Особенности Реализации

Доступ к котам ограничен владельцем. Пользователь видит только свои объекты:

```python
Cat.objects.filter(owner=self.request.user)
```

Владелец кота не передаётся с frontend, а определяется на backend по JWT-токену.

WebSocket-подключение авторизуется через JWT access token в query string:

```text
ws://localhost:8000/ws/chat/?token=ACCESS_TOKEN
```

Backend проверяет токен, определяет пользователя и добавляет соединение в персональную группу:

```text
user_<id>
```

Это позволяет отправлять сообщения конкретному пользователю.

При отправке сообщения backend:

- определяет отправителя по JWT;
- проверяет получателя;
- валидирует текст сообщения;
- сохраняет сообщение в базе данных;
- отправляет сообщение получателю через WebSocket;
- отправляет отправителю подтверждение.

## License

This project was created as a test assignment for evaluation purposes. No open-source license is provided.