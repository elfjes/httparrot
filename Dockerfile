FROM python:3.7-slim-buster

RUN apt-get update \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

COPY . /httparrot

RUN pip install /httparrot
ENTRYPOINT ["bash", "-c", "parrot"]