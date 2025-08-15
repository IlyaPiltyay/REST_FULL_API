from rest_framework import serializers
from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class UserSerializer(serializers.ModelSerializer):
    history_payment = PaymentSerializer(many=True, read_only=True,
                                        source='payments')

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'history_payment']
        extra_kwargs = {
            'password': {'write_only': True}  # Делаем поле 'password' доступным только для записи
        }
