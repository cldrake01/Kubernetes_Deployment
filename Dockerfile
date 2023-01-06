FROM debian:stretch-slim

EXPOSE 8080

FROM python:3.11

ADD main.py /

RUN pip install webhooks

CMD [ "python", "./main.py" ]
