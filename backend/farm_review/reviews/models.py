"""Модуль моделей для аптеки."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Farm(models.Model):
    """Модель аптеки."""

    name = models.CharField(
        max_length=255,
        verbose_name="Название аптеки",
        db_index=True
    )
    url = models.URLField(
        max_length=255,
        verbose_name="Url карточки аптеки",
    )
    reviews_overall = models.IntegerField(
        verbose_name="Количество отзыов",
        blank=False,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Аптека'
        verbose_name_plural = 'Аптеки'


class Review(models.Model):
    """Модель отзывов."""

    author = models.CharField(
        max_length=255,
        verbose_name="Автор отзыва",
        blank=False,
        db_index=True
    )
    farm = models.ForeignKey(
        Farm,
        related_name="farm_review",
        verbose_name="Название аптеки",
        blank=False,
        null=True,
        on_delete=models.CASCADE
    )
    comment = models.TextField(
        verbose_name="Текст комментария",
        blank=False,
        null=True
    )
    stars = models.CharField(
        max_length=255,
        verbose_name="Оценка аптеки",
        blank=False,
    )
    date = models.CharField(
        max_length=255,
        verbose_name="Когда оставлен отзыв",
        blank=False
    )
    resource = models.CharField(
        max_length=100,
        verbose_name="Источник",
        default="Google Maps",
    )

    def __str__(self) -> str:
        return (f"Автор отзыва: {self.author}")

    class Meta:
        ordering = ['-comment']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
