import pytest

from src.secondary.fvp.read.which_task.todolist_memory import TodolistMemory
from src.dependencies import Dependencies
from src.hexagon.fvp.read.which_task import TodolistPort
from src.infra.memory import Memory
from src.shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistMemory(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistMemory.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies
