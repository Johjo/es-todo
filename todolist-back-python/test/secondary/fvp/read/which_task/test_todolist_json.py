from pathlib import Path

import pytest

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from secondary.fvp.read.which_task.todolist_json import TodolistJson
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistJson(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self, json_path: Path):
        self.path = json_path

    @pytest.fixture
    def json_path(self, tmp_path: Path) -> Path:
        return tmp_path / "todolist.json"

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        dependencies = Dependencies.create_empty()
        dependencies = dependencies.feed_adapter(TodolistPort, TodolistJson.factory)
        dependencies = dependencies.feed_path("todolist_json_path", lambda _: self.path)
        return dependencies

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        TodolistSetJson(self.path).save_snapshot(todolist.to_snapshot())