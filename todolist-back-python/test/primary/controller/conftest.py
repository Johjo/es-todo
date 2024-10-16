import pytest
from faker import Faker

from primary.controller.dependencies import Dependencies, inject_use_cases
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def dependencies():
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
