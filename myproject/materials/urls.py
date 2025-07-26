from django.urls import path
from .views import (
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView
)

app_name = 'materials'  # имя приложения

urlpatterns = [
    # Маршруты для курсов
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),


    # Маршруты для уроков
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),

]
