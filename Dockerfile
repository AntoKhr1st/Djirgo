   # Используем базовый образ Python
     FROM python:3.9
     ENV PYTHONDONTWRITEBYTECODE 1
     ENV PYTHONUNBUFFERED 1
     COPY ./requirements.txt /requirements.txt
     RUN pip install -r /requirements.txt
     RUN mkdir /app
     # Указываем рабочую директорию
     WORKDIR /app     
     # Копируем проект в контейнер
     COPY . /app
     RUN apt-get update && apt-get install -y postgresql-client && apt-get clean


     # Запускаем сервер Django
     CMD python Djirgo/manage.py runserver 0.0.0.0:8000
