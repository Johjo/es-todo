import pytest
from faker import Faker
from peewee import Database, SqliteDatabase

from dependencies import Dependencies
from infra.peewee.sdk import SqliteSdk
from primary.controller.read.todolist import TodolistSetReadPort
from secondary.todolist.todolist_set_peewee import TodolistSetReadPeewee
from test.fixture import TodolistBuilder, TodolistFaker
from test.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


class TestTodolistSetReadPeewee(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.sdk = SqliteSdk(self.database)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadPeewee.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Database, lambda _: self.database)
        all_dependencies = all_dependencies.feed_data(data_name="user_key", value=current_user)
        return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=todolist.to_peewee_sdk(),
                                 tasks=[task.to_peewee_sdk() for task in todolist.to_tasks()])
