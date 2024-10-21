from dataclasses import replace

import pytest
from expression import Ok, Error

from hexagon.todolist.write.close_task import CloseTask
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.fixture import TodolistFaker


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return CloseTask(todolist_set)


def test_close_task(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task_old()
    todolist = replace(fake.a_todolist_old(), tasks=[task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, task.key)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[(replace(task, is_open=False))])


def test_close_when_two_task(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task_old(key=1)
    closed_task = fake.a_task_old(key=2)
    todolist = replace(fake.a_todolist_old(), tasks=[first_task, closed_task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, closed_task.key)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[first_task, (replace(closed_task, is_open=False))])


def test_tell_ok_when_close_task(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task_old()
    todolist = replace(fake.a_todolist_old(), tasks=[task])
    todolist_set.feed(todolist)

    response = sut.execute(todolist.name, task.key)

    assert response == Ok(None)


def test_tell_error_if_task_does_not_exist(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    todolist = fake.a_todolist_old()
    todolist_set.feed(todolist)

    task = fake.a_task_old()
    response = sut.execute(todolist.name, task.key)

    assert response == Error(f"The task '{task.key}' does not exist")
