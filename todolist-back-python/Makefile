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
	@echo "update : update from git"
	@echo "check : check code with mypy"
	@echo "create_table : create table first time"
	@echo "freeze : create requirements.txt"
	@echo "install : install package from requirements.txt"


.PHONY: start
start:
	poetry run python src/start_web_for_test.py

.PHONY: create_table
create_table:
	poetry run python src/create_tables.py

.PHONY: update
update:
	git pull

.PHONY: check
check:
	poetry run mypy . --strict --disallow-untyped-decorators


