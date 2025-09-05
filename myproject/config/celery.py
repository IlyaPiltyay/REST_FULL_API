from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')  # или 'myproject', если ваш проект называется myproject

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'block-inactive-users-every-month': {
        'task': 'myproject.users.tasks.block_inactive_users',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),  # Выполнять 1-го числа каждого месяца
    },
}