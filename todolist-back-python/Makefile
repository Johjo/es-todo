SHELL := /bin/bash
.SHELLFLAGS = -e -c
.SILENT:
.ONESHELL:

.EXPORT_ALL_VARIABLES:
ROOT_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "start : start server"
	@echo "start-demo" start the demo server
	@echo "update : update from git"
	@echo "check : check code with mypy"
	@echo "create_table : create table first time"
	@echo "freeze : create requirements.txt"
	@echo "install : install package from requirements.txt"


.PHONY: start
start:
	python -m pipenv run start_web_for_test.py

.PHONY: start-demo
start-demo:
	python -m fastapi dev .\start_demo.py

.PHONY: create_table
create_table:
	python -m pipenv run create_tables.py

.PHONY: freeze
freeze:
	python -m pipenv run pip freeze > requirements.txt

.PHONY: install
install:
	python -m pipenv run pip install -r requirements.txt


.PHONY: update
update:
	git pull

.PHONY: check
check:
	mypy . --strict --disallow-untyped-decorators


