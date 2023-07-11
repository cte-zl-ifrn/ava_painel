FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y && apt -y install curl 

ADD requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt


ADD requirements-dev.txt /apps/req/requirements-dev.txt
WORKDIR /apps/req
# COPY --from=django-adminlte3 / /apps/django-adminlte3
RUN pip install -r requirements-dev.txt

# FIX: bug on corsheaders
# RUN echo 'import django.dispatch;check_request_enabled = django.dispatch.Signal()' > /usr/local/lib/python3.10/site-packages/corsheaders/signals.py

ADD . /apps/app

EXPOSE 8000
# ENTRYPOINT [ "executable" ]
WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
