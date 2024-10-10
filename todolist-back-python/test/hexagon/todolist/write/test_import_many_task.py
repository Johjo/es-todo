from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TodolistSetPort, TaskSnapshot
from hexagon.todolist.write.reword_task import RewordTask
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate
from test.hexagon.todolist.conftest import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: str, tasks: list[TaskSnapshot]):
        update = lambda todolist: todolist.import_tasks(tasks)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)


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


def test_reword_when_existing_task(sut: ImportManyTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
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
