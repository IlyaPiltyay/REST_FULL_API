from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название курса')
    preview = models.ImageField(upload_to='courses/previews/', null=True, blank=True, verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание курса')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(upload_to='lessons/previews/', null=True, blank=True, verbose_name='Превью')
    video_link = models.URLField(max_length=200, verbose_name='Ссылка на видео')

    def __str__(self):
        return self.name
