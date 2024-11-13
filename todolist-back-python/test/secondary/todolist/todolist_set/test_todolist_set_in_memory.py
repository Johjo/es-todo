import pytest

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from infra.memory import Memory
from secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetInMemory(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        return all_dependencies

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        self.memory.save(todolist.to_snapshot())
