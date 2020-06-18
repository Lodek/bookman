.PHONY: test

test:
	docker-compose run app python -m unittest discover -s tests
