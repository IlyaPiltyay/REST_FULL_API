FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python с помощью Poetry
RUN poetry install --no-root

# Копируем исходный код приложения в контейнер
COPY ./myproject /app/myproject

# Определяем переменные окружения
ENV SECRET_KEY="django-insecure-3go67lh0+!6ymf%ivk770n*ta745&=#&3w=jj6^uyu+7jb*cf0"
ENV CELERY_BROKER_URL="redis://redis:6379/0"
ENV CELERY_BACKEND="redis://redis:6379/0"
ENV DJANGO_SETTINGS_MODULE=myproject.config.settings
ENV PYTHONPATH="/app/myproject:/app"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]