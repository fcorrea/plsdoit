FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install python3 python3-dev python3-pip locales -y && \
	pip3 install pipenv && \
	locale-gen en_US.UTF-8

COPY . /app

WORKDIR /app

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pipenv install --system

CMD FLASK_APP=. flask run
