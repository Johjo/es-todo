import pytest
from faker import Faker

from test.hexagon.todolist.fixture import TodolistSetForTest
from test.fixture import TodolistFaker


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()

@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
