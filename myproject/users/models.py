from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')  # Электронная почта как поле для авторизации
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='аватар')  # Поле для аватара
    phone_number = models.CharField(max_length=15, null=True, blank=True,
                                    verbose_name='телефон')  # Поле для номера телефона
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='город')  # Поле для города

    USERNAME_FIELD = 'email'  # Указание, что электронная почта является именем пользователя
    REQUIRED_FIELDS = []  # Необязательные поля для создания суперпользователя

    def __str__(self):
        return self.email
