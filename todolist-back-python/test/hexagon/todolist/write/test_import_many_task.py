from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.write.import_many_task import ImportManyTask, ExternalTodoListPort
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return ImportManyTask(todolist_set)


class ExternalTodolistForTest(ExternalTodoListPort):
    def __init__(self) -> None:
        self._tasks: list[TaskSnapshot] | None = None

    def all_tasks(self) -> list[TaskSnapshot]:
        if self._tasks is None:
            raise Exception("fed task before")
        return self._tasks

    def feed(self, *tasks: TaskSnapshot):
        self._tasks = tasks


@pytest.fixture
def external_todolist() -> ExternalTodolistForTest:
    return ExternalTodolistForTest()


def test_import_many_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                          external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    expected_tasks = [fake.a_task(1), fake.a_task(2)]
    external_todolist.feed(*expected_tasks)

    todolist = replace(fake.a_todolist(), tasks=[])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, external_todolist)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


def test_import_many_task_when_existing_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                             external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    first_task = fake.a_task(key=1)
    expected_task = fake.a_task(key=2)
    external_todolist.feed(expected_task)
    todolist = replace(fake.a_todolist(), tasks=[first_task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, external_todolist)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[first_task, expected_task])


def test_tell_ok_when_import_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    imported_tasks = [fake.a_task(1), fake.a_task(2)]
    external_todolist.feed(*imported_tasks)
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    response = sut.execute(todolist.name, external_todolist)

    assert response == Ok(None)


def test_tell_error_when_todolist_doest_not_exist(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    external_todolist.feed(fake.a_task(1))
    response = sut.execute("unknown_todolist", external_todolist)

    assert response == Error("todolist not found")
