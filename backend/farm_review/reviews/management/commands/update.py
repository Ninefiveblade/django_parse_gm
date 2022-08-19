"""Файл загрузки даных в базу данных проекта."""
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews import models

data = os.path.join(settings.BASE_DIR, "data")


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
