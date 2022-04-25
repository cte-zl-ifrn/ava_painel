FROM python:3.10.2-slim-bullseye

ENV PYTHONUNBUFFERED 1

ADD src/python/requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
