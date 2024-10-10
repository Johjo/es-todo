from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.write.import_many_task import ImportManyTask
from test.hexagon.todolist.conftest import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return ImportManyTask(todolist_set)


def test_import_many_task(sut: ImportManyTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    expected_tasks = [fake.a_task(1), fake.a_task(2)]
    todolist = replace(fake.a_todolist(), tasks=[])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, expected_tasks)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


def test_import_many_task_when_existing_task(sut: ImportManyTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task(key=1)
    expected_task = fake.a_task(key=2)
    todolist = replace(fake.a_todolist(), tasks=[first_task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, [expected_task])

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[first_task, expected_task])


def test_tell_ok_when_import_task(sut: ImportManyTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    imported_tasks = [fake.a_task(1), fake.a_task(2)]
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    response = sut.execute(todolist.name, imported_tasks)

    assert response == Ok(None)


def test_tell_error_when_todolist_doest_not_exist(sut: ImportManyTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    response = sut.execute("unknown_todolist", [fake.a_task(1)])

    assert response == Error("todolist not found")
