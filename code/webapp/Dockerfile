FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN apt-get update && \
	apt-get install python3 python3-dev python3-pip locales python3-mysqldb -y && \
	pip3 install pipenv && \
	echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
	locale-gen

COPY . /app

RUN ln -s ./app/static ./static

WORKDIR /app

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pipenv install --system

#ENTRYPOINT ./entrypoint.sh
