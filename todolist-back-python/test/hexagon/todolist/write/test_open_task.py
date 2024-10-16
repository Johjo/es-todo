from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TaskSnapshot, TaskKey
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from hexagon.todolist.write.open_task import OpenTaskUseCase
from test.hexagon.todolist.conftest import todolist_set
from test.hexagon.todolist.fixture import TodolistSetForTest, a_todolist_snapshot, a_task_key, a_task, TodolistFaker


class TaskKeyGeneratorForTest(TaskKeyGeneratorPort):
    def __init__(self) -> None:
        self.key :TaskKey | None= None

    def feed(self, key: TaskKey) -> None:
        self.key = key

    def generate(self) -> TaskKey:
        assert self.key, f"key must be fed before generating"
        return self.key


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> OpenTaskUseCase:
    return OpenTaskUseCase(todolist_set, task_key_generator)


def test_open_task_when_no_task(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()

    task_key_generator.feed(expected_task.key)

    sut.execute(todolist_name=todolist.name, name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    first_task = fake.a_task(key=1)
    expected_task = fake.a_task(key=2)

    initial = replace(a_todolist_snapshot("my_todolist"), tasks=[first_task])
    todolist_set.feed(initial)

    task_key_generator.feed(expected_task.key)


    sut.execute(todolist_name="my_todolist", name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == replace(initial, tasks=[first_task, expected_task])


def test_tell_ok_when_open_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    initial = a_todolist_snapshot("my_todolist")
    todolist_set.feed(initial)
    task_key_generator.feed(fake.a_task().key)


    response = sut.execute(todolist_name="my_todolist", name="buy the milk")

    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut, todolist_set):
    response = sut.execute(todolist_name="my_todolist", name="buy the milk")

    assert response == Error("todolist not found")
