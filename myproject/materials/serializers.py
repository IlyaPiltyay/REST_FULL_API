from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_link_validator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[youtube_link_validator])

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {"owner": {"read_only": True}}


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {"owner": {"read_only": True}}

    def get_count_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
