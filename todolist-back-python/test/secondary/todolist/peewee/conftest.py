import pytest
from faker import Faker
from peewee import SqliteDatabase  # type: ignore

from secondary.todolist.table import Task, Todolist
from test.fixture import TodolistFaker


# todo: delete this autouse
@pytest.fixture(autouse=True)
def peewee_database():
    database = SqliteDatabase(':memory:')
    database.connect()
    created_table = [Todolist, Task]
    with database.bind_ctx(created_table):
        database.create_tables(created_table)
    return database


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())
