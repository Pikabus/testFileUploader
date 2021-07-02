FROM python:3.8

COPY ./app /usr/src/app

COPY ./requirements.txt /usr/src/

RUN pip3 install --upgrade pip

RUN pip3 install -r /usr/src/requirements.txt

WORKDIR /usr/src

CMD gunicorn --bind 0.0.0.0:5000 app.main:app -w 4 -k uvicorn.workers.UvicornWorker --reload --access-logfile - --error-logfile - --log-level info