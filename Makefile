.PHONY: test source

test: source
	python -m unittest tests

source:
	source .secrets
