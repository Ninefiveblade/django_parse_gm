"""Файл загрузки даных в базу данных проекта."""
import os
import json

from django.core.management.base import BaseCommand
from tqdm import tqdm

from reviews import models

data = os.path.abspath("../data")


class Command(BaseCommand):
    """Comand for deploy data to database."""

    def handle(self, *args, **options):
        models.Farm.objects.all().delete()
        models.Review.objects.all().delete()
        with open(f"{data}/dump.json", "r") as j:
            data_dict = json.loads(j.read())
            farmacy = models.Farm.objects.get_or_create(
                id=1,
                name=data_dict["pharmacy"][0][:18],
                url=data_dict["pharmacy_url"][0][:254],
                reviews_overall=data_dict["reviews_overall"][0],
            )
            try:
                count = 0
                for a in tqdm(data_dict["reviews"]):
                    count += 1
                    models.Review.objects.get_or_create(
                        id=count,
                        author=a.get("name"),
                        comment=a.get("comment"),
                        stars=a.get("stars"),
                        date=a.get("date"),
                        farm=farmacy[0]
                    )
                print("Загрузка Отзывов завершена! "
                      f"Загружено товаров: {len(data_dict)}")
            except Exception as er:
                print("Что-то не так с моделями, путями или базой данных "
                      f"проверьте, ошибка: {er}")
