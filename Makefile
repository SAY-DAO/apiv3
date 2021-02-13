SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: help
help:		    ## Display this help message
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

.PHONY: migrate
migrate: 		## Migrate db
	poetry run ./api/manage.py migrate

.PHONY: makemigrations
makemigrations: 	## Make migrations
	poetry run ./api/manage.py makemigrations

.PHONY: server
server: 		## Run server
	poetry run ./api/manage.py runserver

.PHONY: test
test: 		## Run tests
	poetry run ./api/manage.py test

