import pytest
from faker import Faker
from peewee import SqliteDatabase

from secondary.todolist.table import Task, database_proxy, Todolist
from test.fixture import TodolistFaker


@pytest.fixture(autouse=True)
def database():
    database = SqliteDatabase(':memory:')
    database_proxy.initialize(database)
    return database


@pytest.fixture(autouse=True)
def create_tables(database):
    database.connect()
    database.create_tables([Todolist, Task])


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())
