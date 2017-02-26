FROM python:3.5.2-alpine

RUN mkdir -p /usr/src/app

ADD . /usr/src/app/

# CMD [ "python", "mule.py" ]
