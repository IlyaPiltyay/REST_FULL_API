from rest_framework import serializers

from .models import CustomUser, Payment
from ..materials.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):

    paid_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    paid_lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    history_payment = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "history_payment"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }  # Делаем поле 'password' доступным только для записи
        }
