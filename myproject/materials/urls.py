from rest_framework.routers import SimpleRouter
from django.urls import path

from .apps import MaterialsConfig
from .views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonDestroyAPIView,
    SubscriptionView,  # Если у вас есть отдельный SubscriptionView, оставьте его
)

app_name = MaterialsConfig.name  # имя вашего приложения

# Создаем роутер
router = SimpleRouter()
router.register(
    r"courses", CourseViewSet, basename="course"
)  # Регистрация маршрута для курсов

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("courses/<int:course_id>/subscribe/", CourseViewSet.as_view({'post': 'subscribe'}), name="course_subscribe"),
]

# Включаем маршруты роутера
urlpatterns += router.urls
