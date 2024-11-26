from sqlite3 import Connection

import pytest
from peewee import SqliteDatabase, sqlite3  # type: ignore

from infra.peewee.sdk import SqliteSdk
from infra.peewee.table import Todolist as TodolistActual, Task as TaskActual, Session as FvpSessionActual
from infra.peewee.table import Todolist as TodolistPrevious, Task as TaskPrevious, \
    Session as FvpSessionPrevious

@pytest.mark.skip
def test_migration():
    # GIVEN
    actual_tables = [TodolistActual, TaskActual, FvpSessionActual]
    previous_database = create_peewee_database(actual_tables)

    previous = describe_database(previous_database)

    actual_database = SqliteDatabase(':memory:')
    sdk = SqliteSdk(database=actual_database)
    sdk.create_tables()

    assert describe_database(previous_database) == describe_database(actual_database)

    # previous = "\n".join([str(row) for row in cursor.fetchall()])

    # # THEN
    # assert database_actual.get_tables()
    # assert database_actual.get_tables() == database_previous.get_tables()
    # for table in database_actual.get_tables():
    #     assert database_previous.get_columns(table) == database_actual.get_columns(table), f"wrong column for {table}"
    #     assert database_previous.get_indexes(table) == database_actual.get_indexes(table), f"wrong index for {table}"
    #     assert database_previous.get_primary_keys(table) == database_actual.get_primary_keys(table), f"wrong primary key for {table}"
    #     assert database_previous.get_foreign_keys(table) == database_actual.get_foreign_keys(table), f"wrong foreign key for {table}"


def describe_database(database_actual):
    cursor = database_actual.cursor()
    cursor.execute("SELECT sql FROM sqlite_schema")
    return "\n".join([str(row) for row in cursor.fetchall()])


def create_initial_sqlite():
    pass




def create_peewee_database(actual_tables):
    database_actual = SqliteDatabase(':memory:')
    database_actual.connect()
    with database_actual.bind_ctx(actual_tables):
        database_actual.create_tables(actual_tables)
    return database_actual

# table version
# description des tables
#