from datetime import datetime

import pytest
from expression import Ok, Error, Some

from src.hexagon.shared.event import TaskPostponedEvent
from src.hexagon.shared.type import TaskExecutionDate, TaskKey
from src.hexagon.todolist.write.postpone_task import PostPoneTask
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.fixture
def sut(todolist_set: TodolistSetForTest) -> PostPoneTask:
    return PostPoneTask(todolist_set)


def test_save_postponed_task(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=(task,))
    todolist_set.feed(todolist)

    today = datetime.today()
    sut.execute(todolist.to_name(), task.to_key(), TaskExecutionDate(today))

    actual = todolist_set.by(todolist.to_name()).value
    assert actual == todolist.having(tasks=(task.having(execution_date=Some(TaskExecutionDate(today))),)).to_snapshot()


def test_postpone_task_when_two_tasks(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task_1 = fake.a_task()
    task_2 = fake.a_task()
    postponed_task = fake.a_task()

    todolist = fake.a_todolist().having(tasks=[task_1, postponed_task, task_2])
    todolist_set.feed(todolist)

    today = TaskExecutionDate(datetime.today())
    sut.execute(todolist.name, postponed_task.to_key(), today)

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(
        tasks=[task_1, postponed_task.having(execution_date=Some(today)), task_2]).to_snapshot()


def test_tell_ok_when_postpone_task(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    execution_date = fake.a_date()
    response = sut.execute(todolist.name, TaskKey(task.to_key()), TaskExecutionDate(execution_date))

    assert response == Ok((TaskPostponedEvent(task_key=task.to_key(), execution_date=execution_date), ))


def test_tell_error_when_task_not_found(sut: PostPoneTask, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    unknown_task = fake.a_task()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    today = datetime.today()
    response = sut.execute(todolist.name, TaskKey(unknown_task.to_key()), TaskExecutionDate(today))

    assert response == Error(f"The task '{unknown_task.to_key()}' does not exist")