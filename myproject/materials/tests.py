from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import sys
import os
# from myproject.materials.models import Course, Lesson, Subscription
# Были проблемы с импортом, смог решить только таким способом
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Теперь можно импортировать
from materials.models import Course, Lesson, Subscription


class LessonTests(APITestCase):

    def setUp(self) -> None:
        User = get_user_model()

        # Создаем администратора
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Создаем курс
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.admin_user
        )
        self.lesson = Lesson.objects.create(
            name="Initial Lesson",
            description="Initial Description",
            course=self.course,
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.admin_user,
        )

    def test_create_lesson(self):
        """Тестирование создания уроков"""
        self.client.force_authenticate(user=self.admin_user)

        data = {
            "name": "test lesson",
            "description": "test description",
            "course": self.course.id,  # ID курса
            "video_link": "https://www.youtube.com/test",
        }

        response = self.client.post(
            reverse("materials:lesson_create"), data=data, format="json"
        )

        print(response.json())  # Выводить сообщение ответа для отладки
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )  # Проверка на успешное создание

    def test_list_lessons(self):
        """Тестирование списка уроков"""
        self.client.force_authenticate(
            user=self.admin_user
        )  # Аутентификация администратора

        response = self.client.get(reverse("materials:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_lesson(self):
        """Тестирование получения одного урока"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            reverse("materials:lesson_retrieve", args=[self.lesson.id])
        )

        print(response.data)  # Вывод данных, которые возвращает API
        print(response.status_code)  # Вывод статус-кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        # Вывод перед обновлением
        print(f"Authenticated User: {self.admin_user.email}")  # Проверка пользователя
        print(f"Lesson Owner: {self.lesson.owner.email}")  # Проверка владельца урока

        data = {
            "name": "Updated Lesson",
            "description": "Updated Description",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }

        response = self.client.put(
            reverse("materials:lesson_update", args=[self.lesson.id]),
            data=data,
            format="json",
        )

        print(f"Response Status: {response.status_code}")  # Возвращаемый статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson")


class SubscriptionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        self.course = Course.objects.create(
            name="Test Course", description="Test Description"
        )

    def test_add_subscription(self):
        """Тестирование добавления подписки на курс"""
        url = reverse("materials:lesson_list")
        response = self.client.post(url, {"course_id": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_remove_subscription(self):
        """Тестирование удаления подписки с курса"""
        Subscription.objects.create(
            user=self.user, course=self.course
        )  # Сначала создаем подписку

        url = reverse("materials:lesson_list")
        response = self.client.post(url, {"course_id": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_already_subscribed_message(self):
        """Тестирование сообщения, если пользователь уже подписан на курс"""
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("materials:lesson_list")
        response = self.client.post(url, {"course_id": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")  # удаление
