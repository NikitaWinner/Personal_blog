from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    """Конкретно-прикладной модельный менеджер"""

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Модель данных для постов блога."""

    class Status(models.TextChoices):
        """Модель для статуса Черновик/Опубликован."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(
        default=timezone.now
    )  # время публикации поста
    created = models.DateTimeField(auto_now_add=True)  # время создания поста
    updated = models.DateTimeField(auto_now=True)  # время обновления поста
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ["-publish"]  # убывающий хронологический порядок
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Функция reverse() будет формировать
        URL-адрес динамически, применяя имя URL-адреса,
        определенное в  шаблонах URL-адресов."""
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    """Модель для хранения комментариев
    пользователей к постам."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
