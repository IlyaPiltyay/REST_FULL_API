import re
from rest_framework import serializers


def youtube_link_validator(value):
    """
    Проверяет, является ли ссылка на youtube.com
    """
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*$'
    if not re.match(youtube_regex, value):
        raise serializers.ValidationError("Ссылка должна быть на youtube.com.")
