FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

USER django-user

WORKDIR /app

COPY . .