from pathlib import Path

import pytest

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetJson(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self, json_path: Path):
        self.path = json_path

    @pytest.fixture
    def json_path(self, tmp_path: Path) -> Path:
        return tmp_path / "test_todolist.json"

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_path("todolist_json_path", lambda _: self.path)
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetJson.factory)
        return all_dependencies

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        sut = TodolistSetJson(self.path)
        sut.save_snapshot(todolist.to_snapshot())
