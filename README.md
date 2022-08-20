# Тестовое задание - парсинг отзывов Google Maps
Проект выполняет парсинг всех отзывов аптеки "Ватиканская Аптека", затем записывает все в модели Django.

## Технологии:
Django 2.2.16, beautifulsoup4 4.11.1, selenium 4.4.3

## Чтобы запустить проект необходимо:

### Установить и активировать виртуальное окружение Python3.9
```python3.9 -m venv venv```
```source venv/bin/activate``` 

### Установить зависимости
```pip install -r /backend/requirements.txt```

### Иметь браузер chrome версии 104
### Запустить парсер 1 раз из папки проекта:
```python parse.py``` 
Дождаться выполнения скрипта.

### Перейти в папку infra 

```cd infra```

### Создать .env файл с данными:

```
SECRET_KEY = 'b(q7-x^=h0)(m40l4*r6#6ux46m#t63&ur7z@fk@2fjv(i*3hd'

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dio27786
DB_HOST=db
DB_PORT=5432
#AuthModel
AUTH_USER_MODEL='users.FoodgramUser'
```

### Запустить docker-compose:

```docker-compose up -d —build```

### Выполнить миграции:

```docker-compose exec backend python manage.py makemigration```
```docker-compose exec backend python manage.py migrate```

### Cобрать статику:

```docker-compose exec backend python manage.py collectstatic```

### Создать суперпользователя:

```docker-compose exec backend python manage.py createsuperuser```

### Зайти в админку:

[127.0.0.1/admin](http://127.0.0.1/admin)

### License:



