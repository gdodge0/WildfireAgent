# syntax=docker/dockerfile:1

FROM python:3.12.7-bookworm

WORKDIR /python-docker

RUN apt-get update && apt-get -y install portaudio19-dev python3-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3000
EXPOSE 8080

ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]