all: deploy

## Deploy locally
.PHONY: deploy
deploy:
	docker-compose up -d --build 2> /dev/null

## Remove all containers
.PHONY: clean
clean:
	docker-compose rm -s -f

_test:
	docker-compose build
	docker-compose run -e MYSQL_DB=test_plsdoit app pytest

## Run tests
.PHONY: test
test: _test clean
