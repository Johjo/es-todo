from pathlib import Path

import pytest
from faker import Faker

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
from secondary.todolist.todolist_set_json import TodolistSetJson
from secondary.todolist.todolist_set_read_json import TodolistSetReadJson
from test.fixture import TodolistFaker, TodolistBuilder
from test.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())



class TestTodolistSetReadJson(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self, json_path: Path):
        self.path = json_path

    @pytest.fixture
    def json_path(self, tmp_path: Path) -> Path:
        return tmp_path / "todolist.json"

    def feed_todolist(self, todolist: TodolistBuilder):
        TodolistSetJson(self.path).save_snapshot(todolist.to_snapshot())

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_path("todolist_json_path", lambda _: self.path)
        all_dependencies = all_dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadJson.factory)
        return all_dependencies


@pytest.fixture
def dependencies(json_path: Path) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: json_path)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadJson.factory)
    return dependencies
