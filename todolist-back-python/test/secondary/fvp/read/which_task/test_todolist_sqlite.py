import sqlite3

import pytest

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from infra.sqlite.sdk import SqliteSdk
from secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite
from shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistSqlite(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._connection = sqlite3.connect(':memory:')
        self._sdk = SqliteSdk(self._connection)
        self._sdk.create_tables()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self._sdk.upsert_todolist(
            user_key=user_key,
            todolist=todolist.to_sqlite_sdk(),
            tasks=[task.to_sqlite_sdk() for task in todolist.to_tasks()])

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistSqlite.factory)
        all_dependencies = all_dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self._connection)
        all_dependencies= all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies
