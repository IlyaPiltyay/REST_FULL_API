from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import CustomUser, Payment
from .serializers import UserSerializer, PaymentSerializer
from .service import create_price, create_sessions, create_product


class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_method",)
    ordering_fields = ["payment_date"]

    @swagger_auto_schema(
        operation_description="Удалить платеж по ID.",
        responses={204: "Платеж успешно удален.", 404: "Платеж не найден."},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Сохраняем платеж и связываем его с пользователем
        payment = serializer.save(user=self.request.user)

        # Проверяем, что amount задан и больше нуля
        if payment.amount is None or payment.amount <= 0:
            raise ValueError("Payment amount must be provided and greater than zero.")

        # Создаем продукт
        product = create_product("Course")

        # Создаем цену в Stripe
        price = create_price(payment.amount)

        # Создаем сессию в Stripe
        session_id, payment_link = create_sessions(price)

        # Обновляем платеж объектами session_id и payment_link
        payment.session_id = session_id
        payment.payment_link = payment_link

        # Сохраняем обновленный объект payment
        payment.save()


class MyTokenObtainPairView(TokenObtainPairView):
    pass  # Использует стандартный функционал


class MyTokenRefreshView(TokenRefreshView):
    pass  # Использует стандартный функционал
