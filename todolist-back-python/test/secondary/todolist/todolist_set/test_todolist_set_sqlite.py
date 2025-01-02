import sqlite3

import pytest

from src.dependencies import Dependencies
from src.hexagon.todolist.port import TodolistSetPort
from src.infra.sqlite.sdk import SqliteSdk
from src.secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite
from src.shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetSqlite(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.connection = sqlite3.connect(':memory:')
        self.sdk = SqliteSdk(self.connection)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetSqlite.factory)
        all_dependencies = all_dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self.connection)
        all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=todolist.to_sqlite_sdk(),
                                 tasks=[task.to_sqlite_sdk() for task in todolist.to_tasks()])
