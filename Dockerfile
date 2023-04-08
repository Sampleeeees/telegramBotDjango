FROM python:3.8

RUN apt-get update && \
    apt-get install -y postgresql && \
    apt-get install -y postgresql-contrib

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 13042004
ENV POSTGRES_DB tebteam
ENV POSTGRES_HOST localhost

RUN echo "Debug information"
# Запускаем миграции базы данных

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]