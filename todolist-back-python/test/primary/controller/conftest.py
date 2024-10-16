import pytest
from faker import Faker

from primary.controller.dependencies import inject_use_cases
from dependencies import Dependencies
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def dependencies():
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
