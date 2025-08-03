from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from django.urls import path, include

from .views import UserUpdateAPIView, UserDestroyAPIView, UserCreateAPIView, UserRetrieveAPIView, UserListAPIView, \
    PaymentViewSet


app_name = UsersConfig.name  # имя приложения


router = DefaultRouter()
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("users/create/", UserCreateAPIView.as_view(), name="users_create"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path('', include(router.urls)),

]
