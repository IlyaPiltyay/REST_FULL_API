from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .pagination import MyPagination
from .permissions import IsOwner, IsModerator
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework import viewsets, permissions, status
from .task import send_course_update_email


# CRUD для курсов с использованием ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ["destroy"]:
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [
                permissions.IsAuthenticated,
                IsOwner | IsModerator,
            ]
        else:
            self.permission_classes = [permissions.IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        # Отправляем уведомление о создании нового курса
        send_course_update_email.delay(new_course.id)

    def perform_update(self, serializer):
        updated_course = serializer.save()
        # Отправляем уведомление об обновлении курса
        send_course_update_email.delay(updated_course.id)

    def subscribe(self, request, course_id=None):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден.'}, status=status.HTTP_404_NOT_FOUND)

        # Обработка подписки
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)

        if created:
            return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already subscribed'}, status=status.HTTP_400_BAD_REQUEST)


# CRUD для уроков с использованием generic
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_description="Удалить урок по ID.",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Урок успешно удален."
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="Урок не найден."),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Доступ запрещен, если пользователь не является владельцем урока."
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriptionView(APIView):
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]  # Проверка аутентификации пользователя

    @swagger_auto_schema(
        operation_description="Добавить или удалить подписку на курс.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса"
                )
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Статус операции",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            status.HTTP_404_NOT_FOUND: "Курс не найден.",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя
        course_id = request.data.get("course_id")  # Получаем ID курса из данных запроса
        course_item = get_object_or_404(
            Course, id=course_id
        )  # Получаем курс из базы данных

        # Получаем объекты подписки текущего пользователя на данный курс
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка существует, то удаляем ее
        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = "Подписка удалена"
        else:
            # Если подписки нет, создаем новую
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        # Возвращаем ответ в API
        return Response({"message": message}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получить подписки текущего пользователя.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Список подписок",
                schema=SubscriptionSerializer(many=True),
            )
        },
    )
    def get(self, request):
        queryset = Subscription.objects.filter(
            user=request.user
        )  # Получаем подписки текущего пользователя

        # Пагинация
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(
            queryset, request
        )  # Пагинируем запрос

        # Сериализация данных
        serializer = SubscriptionSerializer(paginated_queryset, many=True)

        # Возвращаем ответ с пагинацией
        return paginator.get_paginated_response(serializer.data)
