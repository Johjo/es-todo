from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.write.import_many_task import ImportManyTask, ExternalTodoListPort, TaskImported
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.fixture import TodolistFaker


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()

@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> ImportManyTask:
    return ImportManyTask(todolist_set, task_key_generator)


class ExternalTodolistForTest(ExternalTodoListPort):
    def __init__(self) -> None:
        self._tasks: list[TaskImported] | None = None

    def all_tasks(self) -> list[TaskImported]:
        if self._tasks is None:
            raise Exception("fed task before")
        return self._tasks

    def feed(self, *tasks: TaskImported):
        self._tasks = tasks


@pytest.fixture
def external_todolist() -> ExternalTodolistForTest:
    return ExternalTodolistForTest()


def test_import_many_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                          external_todolist: ExternalTodolistForTest, fake: TodolistFaker, task_key_generator: TaskKeyGeneratorForTest):
    expected_tasks = [fake.a_task_old(1), fake.a_task_old(2)]
    external_todolist.feed(*to_imported_task_list(expected_tasks))
    task_key_generator.feed(*[task for task in expected_tasks])
    todolist = replace(fake.a_todolist_old(), tasks=[])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, external_todolist)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


def test_import_many_task_when_existing_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                             external_todolist: ExternalTodolistForTest, fake: TodolistFaker, task_key_generator: TaskKeyGeneratorForTest):
    first_task = fake.a_task_old(key=1)
    expected_task = fake.a_task_old(key=2)
    external_todolist.feed(to_imported_task(expected_task))
    task_key_generator.feed(expected_task)
    todolist = replace(fake.a_todolist_old(), tasks=[first_task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, external_todolist)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[first_task, expected_task])


def test_tell_ok_when_import_task(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker, task_key_generator: TaskKeyGeneratorForTest):
    imported_tasks = [fake.a_task_old(1), fake.a_task_old(2)]
    external_todolist.feed(*to_imported_task_list(imported_tasks))
    task_key_generator.feed(*imported_tasks)
    todolist = fake.a_todolist_old()
    todolist_set.feed(todolist)


    response = sut.execute(todolist.name, external_todolist)

    assert response == Ok(None)


def test_tell_error_when_todolist_doest_not_exist(sut: ImportManyTask, todolist_set: TodolistSetForTest,
                                                  external_todolist: ExternalTodolistForTest, fake: TodolistFaker):
    external_todolist.feed(to_imported_task(fake.a_task_old(1)))
    response = sut.execute("unknown_todolist", external_todolist)

    assert response == Error("todolist not found")


def to_imported_task_list(expected_tasks):
    return [to_imported_task(task) for task in expected_tasks]


def to_imported_task(task: TaskSnapshot) -> TaskImported:
    return TaskImported(name=task.name, is_open=task.is_open)
