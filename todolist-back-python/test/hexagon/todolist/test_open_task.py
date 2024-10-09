from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.aggregate import TaskSnapshot, Task
from hexagon.todolist.open_task import OpenTask
from test.hexagon.todolist.fixture import TodolistSetForTest, a_todolist_snapshot, a_task_key


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()

@pytest.fixture
def sut(todolist_set) -> OpenTask:
    return OpenTask(todolist_set)


def test_open_task_when_no_task(sut : OpenTask, todolist_set: TodolistSetForTest):
    expected_task = Task(key=a_task_key(1), name="buy the milk")

    initial = a_todolist_snapshot("my_todolist")
    expected = replace(initial, tasks=[TaskSnapshot(key=expected_task.key, name=expected_task.name)])
    todolist_set.feed(initial)

    sut.execute(key=expected_task.key, name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == expected


def test_open_task_when_one_task(sut, todolist_set):
    initial_task = TaskSnapshot(key=a_task_key(1), name="buy the milk")
    expected_task = TaskSnapshot(key=a_task_key(2), name="buy the eggs")

    initial = replace(a_todolist_snapshot("my_todolist"), tasks=[initial_task])
    todolist_set.feed(initial)

    sut.execute(key=expected_task.key, name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == replace(initial, tasks=[initial_task, expected_task])


def test_tell_ok_when_open_task(sut, todolist_set):
    initial = a_todolist_snapshot("my_todolist")
    todolist_set.feed(initial)

    response = sut.execute(key=a_task_key(1), name="buy the milk")

    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut, todolist_set):
    response = sut.execute(key=a_task_key(1), name="buy the milk")

    assert response == Error("todolist not found")

