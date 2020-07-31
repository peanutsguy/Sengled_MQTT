FROM python:alpine3.7
WORKDIR  /config
COPY . /app
WORKDIR ../app
RUN pip3 install -r requirements.txt
CMD python3 ./app/mqttsengled.py