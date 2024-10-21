from dataclasses import replace

import pytest
from peewee import Database

from primary.controller.read.todolist import Task
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from test.fixture import TodolistFaker
from test.secondary.todolist.peewee.conftest import peewee_database
from test.secondary.todolist.peewee.fixture import feed_todolist


@pytest.fixture
def sut(peewee_database: Database) -> TodolistSetPeewee:
    return TodolistSetPeewee(peewee_database)


def test_read_task_by(fake: TodolistFaker, peewee_database: Database):
    task_snapshot = fake.a_task_old()
    todolist = replace(fake.a_todolist_old(), tasks=[task_snapshot])
    expected_task = Task(id=task_snapshot.key, name=task_snapshot.name, is_open=task_snapshot.is_open)
    feed_todolist(todolist, peewee_database)

    sut = TodolistSetPeewee(peewee_database)
    assert sut.task_by(todolist.name, expected_task.id) == expected_task


def test_read_all_by_name(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    todolist_1 = fake.a_todolist_old()
    todolist_2 = fake.a_todolist_old()
    todolist_3 = fake.a_todolist_old()
    feed_todolist(todolist_1, peewee_database)
    feed_todolist(todolist_2, peewee_database)
    feed_todolist(todolist_3, peewee_database)

    assert sut.all_by_name() == [todolist_1.name, todolist_2.name, todolist_3.name]


def test_read_counts_by_context(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    todolist = replace(fake.a_todolist_old(),
                       tasks=[replace(fake.a_task_old(), name="title #context1 #context2"),
                              replace(fake.a_task_old(), name="#Con_Text3 title #context2"),
                              replace(fake.a_task_old(), name="@ConText4 title"),
                              replace(fake.a_task_old(), name="@Con-Text5 title #context2"),
                              ])
    feed_todolist(todolist, peewee_database)

    assert sut.counts_by_context(todolist.name) == [("#context1", 1), ("#context2", 3), ("#con_text3", 1),
                                                    ("@context4", 1), ("@con-text5", 1)]


def test_read_all_tasks(sut: TodolistSetPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task(), fake.a_task()]
    todolist_1 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
    todolist_2 = fake.a_todolist().having(tasks=expected_tasks)
    todolist_3 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
    TodolistSetPeewee(peewee_database).save_snapshot(todolist_1.to_snapshot())
    TodolistSetPeewee(peewee_database).save_snapshot(todolist_2.to_snapshot())
    TodolistSetPeewee(peewee_database).save_snapshot(todolist_3.to_snapshot())

    actual = sut.all_tasks(todolist_2.name)
    assert actual == [task.to_task() for task in expected_tasks]