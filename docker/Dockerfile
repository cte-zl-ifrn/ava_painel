FROM python:3.10.2-slim-bullseye

ENV PYTHONUNBUFFERED 1

ADD requirements.txt . 

RUN pip install --upgrade pip 
RUN pip install -r /requirements.txt

ADD startup.sh .

WORKDIR /apps/app
CMD /startup.sh
