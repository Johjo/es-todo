import sqlite3

import pytest

@pytest.mark.skip
def test_migration():
    pass
    # # GIVEN
    # actual_tables = [TodolistActual, TaskActual, FvpSessionActual]
    #
    # previous = describe_database(previous_database)
    #
    # actual_database = SqliteDatabase(':memory:')
    # sdk = SqliteSdk(connection=actual_database)
    # sdk.create_tables()
    #
    # assert describe_database(previous_database) == describe_database(actual_database)

    # previous = "\n".join([str(row) for row in cursor.fetchall()])

    # # THEN
    # assert database_actual.get_tables()
    # assert database_actual.get_tables() == database_previous.get_tables()
    # for table in database_actual.get_tables():
    #     assert database_previous.get_columns(table) == database_actual.get_columns(table), f"wrong column for {table}"
    #     assert database_previous.get_indexes(table) == database_actual.get_indexes(table), f"wrong index for {table}"
    #     assert database_previous.get_primary_keys(table) == database_actual.get_primary_keys(table), f"wrong primary key for {table}"
    #     assert database_previous.get_foreign_keys(table) == database_actual.get_foreign_keys(table), f"wrong foreign key for {table}"


def describe_database(database_actual: sqlite3.Connection):
    cursor = database_actual.cursor()
    cursor.execute("SELECT sql FROM sqlite_schema")
    return "\n".join([str(row) for row in cursor.fetchall()])
