FROM tiangolo/uvicorn-gunicorn:python3.9

ENV APP_ROOT /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash newuser
USER newuser
WORKDIR /home/newuser

RUN pip install --user --upgrade pip

RUN python3 -m venv venv

CMD ["source", "env/bin/activate"]

WORKDIR ${APP_ROOT}

COPY --chown=newuser:newuser ./requirements.txt /config/requirements.txt

COPY . .

RUN pip install --user --no-cache-dir -r /config/requirements.txt

