import sqlite3

import pytest
from faker import Faker

from src.dependencies import Dependencies
from src.infra.sqlite.sdk import SqliteSdk
from src.primary.controller.read.todolist import TodolistSetReadPort
from src.secondary.todolist.todolist_set_read.todolist_set_read_sqlite import TodolistSetReadSqlite
from src.shared.const import USER_KEY
from test.fixture import TodolistBuilder, TodolistFaker
from test.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


class TestTodolistSetReadSqlite(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._connection = sqlite3.connect(':memory:')
        self.sdk = SqliteSdk(self._connection)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadSqlite.factory)
        all_dependencies = all_dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self._connection)
        all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=todolist.to_sqlite_sdk(),
                                 tasks=[task.to_sqlite_sdk() for task in todolist.to_tasks()])
