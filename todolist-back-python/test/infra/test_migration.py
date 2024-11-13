from peewee import SqliteDatabase, DateField  # type: ignore
from playhouse.migrate import SqliteMigrator, migrate  # type: ignore

from infra.peewee.table import Todolist as TodolistActual, Task as TaskActual, Session as FvpSessionActual
from infra.peewee.table_previous import Todolist as TodolistPrevious, Task as TaskPrevious, \
    Session as FvpSessionPrevious
from migrate import migrate_to_actual


def test_migration():
    # GIVEN
    actual_tables = [TodolistActual, TaskActual, FvpSessionActual]
    previous_tables = [TodolistPrevious, TaskPrevious, FvpSessionPrevious]

    database_actual = create_database(actual_tables)

    # WHEN
    database_previous = create_database(previous_tables)
    migrate_to_actual(database_previous)

    # THEN
    assert database_actual.get_tables()
    assert database_actual.get_tables() == database_previous.get_tables()
    for table in database_actual.get_tables():
        assert database_previous.get_columns(table) == database_actual.get_columns(table), f"wrong column for {table}"
        assert database_previous.get_indexes(table) == database_actual.get_indexes(table), f"wrong index for {table}"
        assert database_previous.get_primary_keys(table) == database_actual.get_primary_keys(table), f"wrong primary key for {table}"
        assert database_previous.get_foreign_keys(table) == database_actual.get_foreign_keys(table), f"wrong foreign key for {table}"


def create_database(actual_tables):
    database_actual = SqliteDatabase(':memory:')
    database_actual.connect()
    with database_actual.bind_ctx(actual_tables):
        database_actual.create_tables(actual_tables)
    return database_actual

