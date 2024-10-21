from dataclasses import replace

import pytest
from expression import Nothing
from peewee import SqliteDatabase, Database  # type: ignore

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from test.fixture import TodolistFaker
from test.secondary.todolist.peewee.conftest import fake
from test.secondary.todolist.peewee.fixture import feed_todolist


@pytest.fixture
def dependencies(peewee_database: Database) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetPeewee.factory)
    dependencies = dependencies.feed_infrastructure(Database, lambda _: peewee_database)
    return dependencies


@pytest.fixture
def sut(dependencies: Dependencies):
    return dependencies.get_adapter(TodolistSetPort)


def test_get_by_when_one_todolist(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_todolist = fake.a_todolist_old()
    feed_todolist(todolist=expected_todolist, database=peewee_database)

    assert sut.by(expected_todolist.name).value == expected_todolist


def test_get_by_when_two_todolist(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_todolist = fake.a_todolist_old()
    feed_todolist(fake.a_todolist_old(), peewee_database)
    feed_todolist(expected_todolist, peewee_database)

    assert sut.by(expected_todolist.name).value == expected_todolist


def test_get_by_when_todolist_has_tasks(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_todolist = replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()])
    feed_todolist(replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()]), peewee_database)
    feed_todolist(expected_todolist, peewee_database)

    assert sut.by(expected_todolist.name).value == expected_todolist


def test_get_when_todolist_does_not_exist(sut: TodolistSetPeewee, fake: TodolistFaker):
    unknown_todolist = fake.a_todolist_old()
    assert sut.by(unknown_todolist.name) == Nothing


def test_insert_todolist(sut: TodolistSetPeewee, fake: TodolistFaker):
    expected_todolist = replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()])
    sut.save_snapshot(expected_todolist)

    assert sut.by(expected_todolist.name).value == expected_todolist


def test_update_todolist(sut: TodolistSetPeewee, fake: TodolistFaker):
    initial_todolist = replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()])
    sut.save_snapshot(initial_todolist)

    expected_todolist = replace(initial_todolist, tasks=[fake.a_task_old(), fake.a_task_old()])
    sut.save_snapshot(expected_todolist)

    assert sut.by(expected_todolist.name).value == expected_todolist
