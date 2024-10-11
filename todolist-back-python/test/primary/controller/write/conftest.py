import pytest
from faker import Faker

from primary.controller.write.dependencies import Dependencies, inject_use_cases
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def empty_dependencies():
    return Dependencies.create_empty()


# todo: remove this fixture
@pytest.fixture
def dependencies_with_use_cases():
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def dependencies():
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
