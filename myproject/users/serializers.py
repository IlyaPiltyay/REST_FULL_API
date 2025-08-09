from rest_framework import serializers
from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    history_payment = PaymentSerializer(many=True, read_only=True,
                                        source='payments')

    class Meta:
        model = CustomUser
        fields = '__all__'  # Используйте '__all__' для включения всех полей
        extra_kwargs = {
            'password': {'write_only': True}  # Делаем поле 'password' доступным только для записи
        }

