from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.contrib.auth.models import User


@shared_task
def block_inactive_users():
    # Определяем время, когда пользователь считается неактивным
    threshold = timezone.now() - timedelta(days=30)
    # Находим всех пользователей, которые не заходили более 30 дней
    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)

    # Блокируем найденных пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} был заблокирован из-за неактивности.")
