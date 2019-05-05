all: deploy

## Deploy locally
.PHONY: deploy
deploy:
	docker-compose up -d --build

## Remove all containers
.PHONY: clean
clean:
	docker-compose rm -s -f

_test:
	docker-compose -f test.yaml up

## Run tests
.PHONY: test
test: _test clean

## Sample data
.PHONY: sample-data
sample-data: 
	docker-compose exec app flask load_sample
