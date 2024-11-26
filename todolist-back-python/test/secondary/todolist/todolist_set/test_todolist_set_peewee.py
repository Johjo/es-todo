from uuid import UUID

import pytest
from peewee import SqliteDatabase, Database  # type: ignore

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from infra.peewee.sdk import SqliteSdk
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetPeewee(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.sdk = SqliteSdk(self.database)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetPeewee.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Database, lambda _: self.database)
        all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=todolist.to_peewee_sdk(),
                                 tasks=[task.to_peewee_sdk() for task in todolist.to_tasks()])
