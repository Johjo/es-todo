from dataclasses import replace

import pytest
from expression import Ok, Error

from src.hexagon.todolist.write.close_task import CloseTask
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest):
    return CloseTask(todolist_set)


def test_close_task(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, task.to_key())

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[task.having(is_open=False)]).to_snapshot()


def test_close_when_two_tasks(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    first_task = fake.a_task(1)
    closed_task = fake.a_task(2)
    todolist = fake.a_todolist().having(tasks=[first_task, closed_task])
    todolist_set.feed(todolist)

    sut.execute(todolist.name, closed_task.to_key())

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[first_task, (replace(closed_task, is_open=False))]).to_snapshot()


def test_tell_ok_when_close_task(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    response = sut.execute(todolist.name, task.to_key())

    assert response == Ok(None)


def test_tell_error_if_task_does_not_exist(sut: CloseTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    task = fake.a_task()
    response = sut.execute(todolist.name, task.to_key())

    assert response == Error(f"The task '{task.to_key()}' does not exist")
