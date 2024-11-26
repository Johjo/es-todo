import pytest
from peewee import Database, SqliteDatabase  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from infra.peewee.sdk import SqliteSdk
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee
from shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistPeewee(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._database = SqliteDatabase(':memory:')
        self._database.connect()
        self._sdk = SqliteSdk(self._database)
        self._sdk.create_tables()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self._sdk.upsert_todolist(
            user_key=user_key,
            todolist=todolist.to_peewee_sdk(),
            tasks=[task.to_peewee_sdk() for task in todolist.to_tasks()])

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistPeewee.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Database, lambda _: self._database)
        all_dependencies= all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies
