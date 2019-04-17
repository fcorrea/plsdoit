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
	docker-compose -f test.yaml up

## Run tests
.PHONY: test
test: _test clean
