# API Yatube
## Описание проекта

Данный проект реализует функционал API для платформы Yatube, включая:
- Создание, получение, обновление и удаление постов;
- Управление группами;
- Работа с комментариями;
- Подписку пользователей.

## Установка и запуск

1. **Клонирование репозитория:**
    ```bash
    git clone <адрес_репозитория>
    cd <имя_папки>
    ```

2. **Создание виртуального окружения и установка зависимостей:**
    ```bash
    python -m venv venv
    ```
    - Для активации виртуального окружения:
      - На Linux/Mac:
        ```bash
        source venv/bin/activate
        ```
      - На Windows:
        ```bash
        venv\Scripts\activate
        ```
    - Установка зависимостей:
        ```bash
        pip install -r requirements.txt
        ```

3. **Применение миграций:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Запуск сервера:**
    ```bash
    python manage.py runserver
    ```

5. **Доступ к документации:**
    Документация API (Redoc) доступна по адресу: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
