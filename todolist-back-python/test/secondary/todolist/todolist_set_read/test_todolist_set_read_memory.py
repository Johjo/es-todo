import pytest
from faker import Faker

from dependencies import Dependencies
from infra.memory import Memory
from primary.controller.read.todolist import TodolistSetReadPort
from secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory
from test.fixture import TodolistFaker, TodolistBuilder
from test.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


class TestTodolistSetReadMemory(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        return all_dependencies

    def feed_todolist(self, todolist: TodolistBuilder):
        self.memory.save(todolist.to_snapshot())