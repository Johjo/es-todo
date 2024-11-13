import pytest
from peewee import Database, SqliteDatabase  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from infra.peewee.sdk import PeeweeSdk
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistPeewee(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._database = SqliteDatabase(':memory:')
        self._database.connect()
        self._sdk = PeeweeSdk(self._database)
        self._sdk.create_tables()

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        self._sdk.upsert_todolist(todolist=todolist.to_peewee_sdk(),
                                  tasks=[task.to_peewee_sdk() for task in todolist.to_tasks()])

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistPeewee.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Database, lambda _: self._database)
        return all_dependencies
