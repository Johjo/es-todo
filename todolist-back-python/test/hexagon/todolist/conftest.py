import pytest
from faker import Faker
from faker.providers import BaseProvider

from hexagon.todolist.aggregate import TaskSnapshot, TaskKey, TodolistSnapshot
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task(self, key: None | int = None) -> TaskSnapshot:
        if key is None:
            key = self.fake.random_int()
        return TaskSnapshot(key=TaskKey(key), name=self.fake.sentence(), is_open=True)

    def a_todolist(self) -> TodolistSnapshot:
        return TodolistSnapshot(name=self.fake.word(), tasks=[])


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
