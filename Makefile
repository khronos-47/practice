ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

# Manually define main variables

ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

# parse additional args for commands

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = project1


HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \


# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash) cd  $(APPLICATION_NAME)
	@cp .env_example .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

db:  ##@Database Create database with docker-compose
	docker compose -f docker-compose_db.yml up -d --remove-orphans

migrate:  ##@Database Do all migrations in database
	cd $(APPLICATION_NAME)/database/models && alembic upgrade $(args)

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

docker_run: ##@Application Run application server in docker 
	docker compose -f docker-compose.yml up

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	cd $(APPLICATION_NAME)/database/models && alembic revision --autogenerate

open_db:  ##@Database Open database inside docker-image
	docker exec -it postgres psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

%::
	echo $(MESSAGE)