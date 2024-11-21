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
	@echo "check : check code with mypy

.PHONY: start
start:
	python -m pipenv run start_web_for_test.py

.PHONY: update
update:
	git pull

.PHONY: check
check:
	mypy . --strict --disallow-untyped-decorators
