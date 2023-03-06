FROM python:3.11.2-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt update && apt -y install curl 

ADD requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt 

# FIX: bug on corsheaders
# RUN echo 'import django.dispatch;check_request_enabled = django.dispatch.Signal()' > /usr/local/lib/python3.10/site-packages/corsheaders/signals.py

ADD . /apps/app

WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
