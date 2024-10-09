from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TaskSnapshot, TodolistSetPort
from hexagon.todolist.open_task import OpenTask
from test.hexagon.todolist.conftest import todolist_set, TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest, a_todolist_snapshot, a_task_key, a_task


@pytest.fixture
def sut(todolist_set) -> OpenTask:
    return OpenTask(todolist_set)


def test_open_task_when_no_task(sut: OpenTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()

    sut.execute(todolist_name=todolist.name, key=expected_task.key, name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task(key=1)
    expected_task = fake.a_task(key=2)

    initial = replace(a_todolist_snapshot("my_todolist"), tasks=[first_task])
    todolist_set.feed(initial)

    sut.execute(todolist_name="my_todolist", key=expected_task.key, name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == replace(initial, tasks=[first_task, expected_task])


def test_tell_ok_when_open_task(sut, todolist_set):
    initial = a_todolist_snapshot("my_todolist")
    todolist_set.feed(initial)

    response = sut.execute(todolist_name="my_todolist", key=a_task_key(1), name="buy the milk")

    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut, todolist_set):
    response = sut.execute(todolist_name="my_todolist", key=a_task_key(1), name="buy the milk")

    assert response == Error("todolist not found")
