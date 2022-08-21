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
        with open(f"{data}/famacy.json", "r") as j:
            data_dict = json.loads(j.read())
            try:
                count = 0
                for a in tqdm(data_dict["farmacy"]):
                    count += 1
                    farmacy = models.Farm.objects.get_or_create(
                        name=a[0]["name"],
                        url=a[1]["link"][:254],
                        rating=a[2]["farm_stars"],
                        reviews_overall=a[3]["overall_reviews"],
                        resource=a[4]["source"]
                    )
                    models.Review.objects.get_or_create(
                        id=count,
                        author=a[5]["author"],
                        date=a[6]["date"],
                        stars=a[7]["stars"],
                        comment=a[8]["comment"][:254],
                        farm=farmacy[0]
                    )
                print("Загрузка аптек и отзывов завершена!")
            except Exception as er:
                print("Что-то не так с моделями, путями или базой данных "
                      f"проверьте, ошибка: {er}")
