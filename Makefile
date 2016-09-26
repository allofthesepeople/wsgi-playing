run: python-clean
	docker-compose up

build:
	docker-compose build

python-clean: build
	docker-compose run app rm -rf app/__pycache__/

.PHONY: python-clean run
