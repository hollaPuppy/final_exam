FROM python:3.9

ENV APP_ROOT /app

WORKDIR ${APP_ROOT}

COPY ./requirements.txt /config/requirements.txt