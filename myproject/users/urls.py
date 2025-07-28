from django.urls import path

from .apps import UsersConfig
from .views import UserUpdateAPIView, UserDestroyAPIView, UserCreateAPIView, UserRetrieveAPIView, UserListAPIView

app_name = UsersConfig.name  # имя приложения


urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("users/create/", UserCreateAPIView.as_view(), name="users_create"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
]

