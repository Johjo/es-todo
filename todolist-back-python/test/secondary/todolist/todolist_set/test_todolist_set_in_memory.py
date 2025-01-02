
import pytest

from src.dependencies import Dependencies
from src.hexagon.todolist.port import TodolistSetPort
from src.infra.memory import Memory
from src.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from src.shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetInMemory(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())
