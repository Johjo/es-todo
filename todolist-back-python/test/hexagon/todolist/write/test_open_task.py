from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.write.open_task import OpenTaskUseCase
from test.hexagon.todolist.conftest import todolist_set
from test.hexagon.todolist.fixture import TodolistSetForTest, a_todolist_snapshot_old, TaskKeyGeneratorForTest
from test.fixture import TodolistFaker


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> OpenTaskUseCase:
    return OpenTaskUseCase(todolist_set, task_key_generator)


def test_open_task_when_no_task(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    todolist = fake.a_todolist_old()
    todolist_set.feed(todolist)
    expected_task = fake.a_task_old()

    task_key_generator.feed(expected_task.key)

    sut.execute(todolist_name=todolist.name, name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    first_task = fake.a_task_old(key=1)
    expected_task = fake.a_task_old(key=2)

    initial = replace(a_todolist_snapshot_old("my_todolist"), tasks=[first_task])
    todolist_set.feed(initial)

    task_key_generator.feed(expected_task.key)


    sut.execute(todolist_name="my_todolist", name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == replace(initial, tasks=[first_task, expected_task])


def test_tell_ok_when_open_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    initial = a_todolist_snapshot_old("my_todolist")
    todolist_set.feed(initial)
    task_key_generator.feed(fake.a_task_old().key)


    response = sut.execute(todolist_name="my_todolist", name="buy the milk")

    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut, todolist_set):
    response = sut.execute(todolist_name="my_todolist", name="buy the milk")

    assert response == Error("todolist not found")
