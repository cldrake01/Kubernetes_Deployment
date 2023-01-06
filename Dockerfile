FROM debian:stretch-slim

EXPOSE 8080

FROM python:3.11

ADD my_script.py /

RUN pip install webhooks

CMD [ "python", "./my_script.py" ]
