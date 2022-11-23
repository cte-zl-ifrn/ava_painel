FROM python:3.10.4-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt update && apt -y install curl 

ADD requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt 

# FIX: bug on corsheaders
# RUN echo 'import django.dispatch;check_request_enabled = django.dispatch.Signal()' > /usr/local/lib/python3.10/site-packages/corsheaders/signals.py

WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
