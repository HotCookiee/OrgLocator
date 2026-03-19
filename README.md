# 🌍 OrgLocator
![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6.4-DC382D?style=flat-square&logo=redis&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.11.9-E92063?style=flat-square&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-2.10.1-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-1.16.5-6BA81E?style=flat-square&logo=alembic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

**Асинхронный FastAPI микросервис для геолокационного поиска организаций**

> Современное решение для управления организациями с пространственным поиском, JWT-аутентификацией и Redis-кешированием

---

## 📋 Содержание


- О проекте
- Возможности
- Технологический стек
- Быстрый старт
- API Endpoints
- Архитектура
- Структура проекта
- Примеры использования
- Разработка
- Производительность
- Безопасность

---

## 🎯 О проекте

**OrgLocator** — современный асинхронный веб-сервис на FastAPI для управления организациями с акцентом на геопространственный поиск.

### Ключевые особенности

- 🗺️ **Геопоиск** — поиск организаций по радиусу или прямоугольной области
- 🔐 **JWT аутентификация** — безопасная система с refresh токенами
- ⚡ **Асинхронность** — полностью async/await архитектура
- 💾 **Redis кеширование** — оптимизация производительности
- 🏗️ **Чистая архитектура** — разделение на слои
- 🔄 **Alembic миграции** — версионирование БД
- 🐳 **Docker ready** — готовое окружение

---

## ✨ Возможности

### 🗺️ Геопространственный поиск

- Поиск организаций по **радиусу** от точки (latitude, longitude, radius)
- Поиск в **прямоугольной области** (min_lat, max_lat, min_lon, max_lon)
- Автоматическое **кеширование** результатов в Redis
- Точные вычисления координатных областей
- Связь организаций с конкретными зданиями (GPS)


### 🔐 Безопасность

- **JWT аутентификация** с access и refresh токенами
- Хеширование паролей через **Argon2**
- HTTP-only cookies для защиты от XSS
- Контроль срока действия токенов
- Механизм отзыва refresh токенов
- Валидация данных через Pydantic

### 🚀 Производительность

- Полностью **асинхронный** код на async/await
- **SQLAlchemy 2.0** с asyncpg драйвером
- **Redis** для кеширования запросов
- Singleton подключения к БД и кешу
- Connection pooling

---

## 🛠 Технологический стек

| Компонент | Технология | Версия | Назначение |
| :-- | :-- | :-- | :-- |
| **Backend** | FastAPI | 0.117.1 | REST API, async endpoints |
| **Language** | Python | 3.11+ | Основной язык |
| **Database** | PostgreSQL | 15+ | Реляционная БД |
| **ORM** | SQLAlchemy | 2.0.43 | Async ORM |
| **Cache** | Redis | 6.4 | Кеширование |
| **Validation** | Pydantic | 2.11.9 | Схемы данных |
| **Auth** | JWT (PyJWT) | 2.10.1 | Аутентификация |
| **Migrations** | Alembic | 1.16.5 | Версионирование БД |
| **Container** | Docker | Latest | Контейнеризация |
| **Orchestration** | Docker Compose | Latest | Multi-container |


---

## 🚀 Быстрый старт

### Требования

```bash
✅ Docker 20.10+
✅ Docker Compose 2.0+
```


### Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/HotCookiee/OrgLocator.git
cd OrgLocator

# 2. Заполните .env файл
cat > .env << EOF
DATABASE_URL= 
POSTGRES_USER= 
POSTGRES_PASSWORD= 
POSTGRES_DB= 
REDIS_HOST= 
REDIS_PORT=6379 # default
JWT_SECRET_KEY= 
ALGORITHM=HS256 # default
EOF

# 3. Запустите все сервисы
docker compose up -d

# 4. Примените миграции
docker compose exec web alembic upgrade head

# 5. Проверьте работу
curl http://localhost:8000/health/liveness
```


### Доступ к приложению

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### 🔐 Аутентификация

| Метод | Endpoint | Описание |
| :-- | :-- | :-- |
| `POST` | `/users/` | Регистрация пользователя |
| `POST` | `/users/login` | Вход (получение JWT токенов) |
| `POST` | `/users/refresh` | Обновление access токена |
| `DELETE` | `/users/by-id/{id}` | Удаление пользователя |

### 🗺️ Геопоиск

```bash
# Поиск по радиусу (5 км от Красной площади)
GET /organizations/search/geo?latitude=55.7558&longitude=37.6173&radius=5000

# Поиск в прямоугольной области
GET /organizations/search/geo?min_lat=55.0&max_lat=56.0&min_lon=37.0&max_lon=38.0
```


### 🏢 CRUD операции

| Ресурс | GET | POST | DELETE |
| :-- | :-- | :-- | :-- |
| **Organizations** | `/organizations/by-id/{id}` | `/organizations/` | `/organizations/by-id/{id}` |
| **Buildings** | `/buildings/by-id/{id}/organizations` | `/buildings/` | `/buildings/by-id/{id}` |
| **Activities** | `/activities/by-id/{id}/organizations/` | `/activities/` | `/activities/by-id/{id}` |


---

## 🏗 Архитектура

```
┌─────────────────────────────────────────┐
│      FastAPI API Layer                  │
│   • JWT Authentication                  │
│   • Pydantic Validation                 │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│      Service Layer                      │
│   • Геовычисления                       │
│   • JWT Management                      │
│   • Redis Caching                       │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│      Repository Layer (DAO)             │
│   • SQLAlchemy Queries                  │
│   • PostgreSQL Access                   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│      Database Layer                     │
│   PostgreSQL • Redis • Alembic          │
└─────────────────────────────────────────┘
```


---

## 📁 Структура проекта

```
OrgLocator/
│
├── 📄 .dockerignore
├── 📄 .env
├── 📄 .gitattributes
├── 📄 .gitignore
├── 📄 alembic.ini
├── 📄 compose.yml
├── 📄 dockerfile
├── 📄 LICENSE
├── 📄 packages.txt
├── 📄 README.md
│
└── 📂 src/
    ├── 📄 main.py
    ├── 📄 core.py
    │
    ├── 📂 endpoints/
    │   ├── users.py
    │   ├── organizations.py
    │   ├── buildings.py
    │   ├── activities.py
    │   └── health.py
    │
    ├── 📂 services/
    │   ├── users.py
    │   ├── organizations.py
    │   └── tools.py
    │
    ├── 📂 repositories/
    │   ├── users.py
    │   ├── organizations.py
    │   ├── tools.py
    │   └── service.py
    │
    ├── 📂 models/
    │   ├── base.py
    │   ├── users.py
    │   ├── organizations.py
    │   ├── buildings.py
    │   ├── activities.py
    │   └── refresh_tokens.py
    │
    ├── 📂 schemas/
    │   ├── user.py
    │   ├── organization.py
    │   ├── building.py
    │   └── activity.py
    │
    ├── 📂 db/
    │   └── connection.py
    │
    ├── 📂 description/
    │   ├── health.py
    │   ├── organization.py
    │   └── selection_by_filter.py
    │
    └── 📂 migrations/
        ├── env.py
        ├── script.py.mako
        └── versions/


📊 Статистика проекта:
├── 📂 Всего каталогов: 8
├── 📄 Всего файлов: ~40
├── 🐍 Python модулей: ~30
├── ⚙️ Конфигурационных файлов: 6
└── 📝 Документации: 2

```


---

## 💡 Примеры использования

### Регистрация и JWT токены

```python
import httpx

async def register_and_login():
    async with httpx.AsyncClient() as client:
        # Регистрация
        await client.post(
            "http://localhost:8000/users/",
            json={
                "name": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123",
                "organizations_id": "uuid-here"
            }
        )
        
        # Вход
        response = await client.post(
            "http://localhost:8000/users/login",
            json={"name": "john_doe", "password": "SecurePass123"}
        )
        tokens = response.json()
        return tokens["access_token"], tokens["refresh_token"]
```


### Геопоиск

```python
async def find_nearby(access_token: str):
    """Поиск в радиусе 5 км от Красной площади"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/organizations/search/geo",
            params={"latitude": 55.7558, "longitude": 37.6173, "radius": 5000},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.json()
```


---

## 🔧 Разработка

### Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r packages.txt
alembic upgrade head
uvicorn src.main:app --reload
```


### Миграции Alembic

```bash
alembic revision --autogenerate -m "Описание"
alembic upgrade head
alembic downgrade -1
```


### Docker команды

```bash
docker compose build
docker compose up -d
docker compose logs -f web
docker compose down
```


---

## 📊 Производительность

| Операция | С Redis | Без Redis | Ускорение |
| :-- | :-- | :-- | :-- |
| Геопоиск по радиусу | **~5ms** | ~50ms | **10x** |
| Получение по ID | **~3ms** | ~20ms | **6x** |
| Поиск по названию | **~4ms** | ~25ms | **6x** |


---

## 🔒 Безопасность

✅ Хеширование паролей через **Argon2**
✅ JWT токены в **HTTP-only cookies**
✅ Короткоживущие access токены (30 минут)
✅ Долгоживущие refresh токены (7 дней)
✅ Валидация через **Pydantic**
✅ SQL injection защита через **SQLAlchemy ORM**



## 📄 Лицензия

Проект распространяется под лицензией **[MIT](LICENSE)**.

---

## 📧 Контакты

**Автор**: [@HotCookiee](https://github.com/HotCookiee)
**Репозиторий**: [OrgLocator](https://github.com/HotCookiee/OrgLocator)
**Issues**: [Сообщить о проблеме](https://github.com/HotCookiee/OrgLocator/issues)

---



