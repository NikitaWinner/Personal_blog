from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Модель данных для постов блога."""

    class Status(models.TextChoices):
        """Модель для статуса Черновик/Опубликован."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # время публикации поста
    created = models.DateTimeField(auto_now_add=True)  # время создания поста
    updated = models.DateTimeField(auto_now=True)  # время обновления поста
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ["-publish"]  # убывающий хронологический порядок
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
