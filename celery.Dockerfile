FROM python:3.8

COPY ./app/celery /usr/src/app/celery

COPY ./app/__init__.py /usr/src/app/

COPY ./app/config.py /usr/src/app/

COPY ./requirements.txt /usr/src/

RUN pip3 install --upgrade pip

RUN pip3 install -r /usr/src/requirements.txt

WORKDIR /usr/src

CMD celery -A app.celery.tasks worker --loglevel=info