# TeamFinder

## О проекте

**TeamFinder** — веб-приложение для поиска команды и совместной работы над pet-проектами.

Пользователи могут:
- создавать собственные проекты;
- искать участников для команды;
- просматривать профили других пользователей;
- присоединяться к проектам;
- добавлять интересные проекты в избранное;
- управлять своим профилем и проектами.

Проект разработан на Django в рамках дипломной работы.

---

# Реализованный функционал

## Пользователи
- регистрация по email;
- авторизация и выход из аккаунта;
- кастомная модель пользователя;
- редактирование профиля;
- смена пароля;
- генерация аватара при регистрации;
- загрузка собственного аватара;
- страница профиля пользователя;
- список всех пользователей.

## Проекты
- создание проектов;
- редактирование проектов;
- просмотр списка проектов;
- детальная страница проекта;
- участие в проектах;
- завершение проекта владельцем;
- пагинация списка проектов.

## Вариант 1
Реализован первый вариант задания:
- добавление проектов в избранное;
- удаление проектов из избранного;
- отдельная страница избранных проектов;
- фильтрация пользователей по связанным проектам.

---

# Технологии

## Backend
- Python 3.12
- Django 5.2.4
- PostgreSQL
- Pillow

## Frontend
- HTML
- CSS
- JavaScript

## Infrastructure
- Docker
- Docker Compose

---

# Установка и запуск проекта

## 1. Клонирование репозитория

```bash
git clone <repository_url>
cd team-finder-ad
```

## 2. Создание виртуального окружения

```bash
python -m venv venv
```

## 3. Активация виртуального окружения

### Windows PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# Настройка переменных окружения

Создайте файл `.env` на основе `.env_example`.

### Windows

```bash
copy .env_example .env
```

### Linux / macOS

```bash
cp .env_example .env
```

Пример заполнения:

```env
DJANGO_SECRET_KEY=django-insecure-secret-key
DJANGO_DEBUG=True

POSTGRES_DB=teamfinder
POSTGRES_USER=teamfinder
POSTGRES_PASSWORD=teamfinder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TASK_VERSION=1
```

## Описание переменных

| Переменная        | Описание                |
| ----------------- | ----------------------- |
| DJANGO_SECRET_KEY | Секретный ключ Django   |
| DJANGO_DEBUG      | Режим разработки        |
| POSTGRES_DB       | Имя базы данных         |
| POSTGRES_USER     | Пользователь PostgreSQL |
| POSTGRES_PASSWORD | Пароль PostgreSQL       |
| POSTGRES_HOST     | Хост PostgreSQL         |
| POSTGRES_PORT     | Порт PostgreSQL         |
| TASK_VERSION      | Номер варианта задания  |

---

# Запуск PostgreSQL через Docker

## Запуск контейнера

```bash
docker compose up -d
```

## Проверка контейнеров

```bash
docker ps
```

## Остановка контейнеров

```bash
docker compose down
```

---

# Миграции

После запуска базы данных выполните:

```bash
python manage.py migrate
```

---

# Создание суперпользователя

```bash
python manage.py createsuperuser
```

Админ-панель будет доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

---

# Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

---

# Основные страницы

| URL                         | Описание               |
| --------------------------- | ---------------------- |
| `/projects/list/`           | Список проектов        |
| `/projects/create-project/` | Создание проекта       |
| `/projects/favorites/`      | Избранные проекты      |
| `/users/register/`          | Регистрация            |
| `/users/login/`             | Вход                   |
| `/users/logout/`            | Выход                  |
| `/users/list/`              | Список пользователей   |
| `/users/edit/`              | Редактирование профиля |
| `/users/change-password/`   | Смена пароля           |
| `/admin/`                   | Django admin           |

---

# Проверка проекта

Проверка Django:

```bash
python manage.py check
```

---

# Особенности реализации

* используется кастомная модель пользователя;
* авторизация реализована по email;
* аватар генерируется автоматически при регистрации;
* медиафайлы пользователей не загружаются в Git;
* используется PostgreSQL вместо SQLite;
* проект адаптирован под Docker Compose.

---

# Примечание для ревьюера

Проект запускался и тестировался на:

* Windows 11;
* Python 3.12;
* Docker Desktop;
* PostgreSQL 16.
