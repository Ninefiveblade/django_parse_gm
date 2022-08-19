"""Модуль моделей для аптеки."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Farm(models.Model):
    pass


class Review(models.Model):
    pass
