import pytest
from faker import Faker

from src.primary.controller.use_case_dependencies import inject_use_cases
from src.dependencies import Dependencies
from test.fixture import TodolistFaker


@pytest.fixture
def dependencies():
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
