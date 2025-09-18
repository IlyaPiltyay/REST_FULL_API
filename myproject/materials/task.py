from celery import shared_task
from django.core.mail import send_mail

from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscription in subscribers:
        send_mail(
            subject=f'Курс "{course.name}" был обновлён!',
            message=f'Здравствуйте, {subscription.user.username}! Курс "{course.name}" был обновлён.',
            from_email=course.owner.email,  # Отправитель
            recipient_list=[subscription.user.email],  # Получатель
            fail_silently=False,
        )
