FROM python:3.10

ENV PYTHONUNBUFFERED 1

ADD requirements.txt . 

RUN pip install --upgrade pip 
RUN pip install --use-feature=2020-resolver -r /requirements.txt

ADD startup.sh .

WORKDIR /apps/app
CMD /startup.sh
