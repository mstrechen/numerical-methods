FROM python:3.6

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-tk

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src /app

EXPOSE 80 8080
ENTRYPOINT [ "bash", "entrypoint.sh" ]