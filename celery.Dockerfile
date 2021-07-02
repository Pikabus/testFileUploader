FROM python:3.8

COPY ./app/celery_app /usr/src/app/celery_app

COPY ./app/__init__.py /usr/src/app/

COPY ./app/config.py /usr/src/app/

COPY ./requirements.txt /usr/src/

RUN pip3 install --upgrade pip

RUN pip3 install -r /usr/src/requirements.txt

WORKDIR /usr/src

CMD celery -A app.celery_app.tasks worker --loglevel=info