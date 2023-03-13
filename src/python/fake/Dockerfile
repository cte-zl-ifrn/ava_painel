FROM python:3.11.2-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt update && apt -y install curl 

ADD requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
