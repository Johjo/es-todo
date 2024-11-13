import pytest
from peewee import SqliteDatabase, Database  # type: ignore

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from infra.peewee.sdk import PeeweeSdk
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetPeewee(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.sdk = PeeweeSdk(self.database)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetPeewee.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Database, lambda _: self.database)
        return all_dependencies

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(todolist=todolist.to_peewee_sdk(),
                                 tasks=[task.to_peewee_sdk() for task in todolist.to_tasks()])
