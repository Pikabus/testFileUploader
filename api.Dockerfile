FROM python:3.8

COPY ./app /usr/src/app

COPY ./requirements.txt /usr/src/

RUN pip3 install --upgrade pip

RUN pip3 install -r /usr/src/requirements.txt

WORKDIR /usr/src

EXPOSE 8000

