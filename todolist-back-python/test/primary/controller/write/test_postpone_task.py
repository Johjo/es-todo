from dataclasses import replace
from datetime import datetime

from expression import Some

from hexagon.shared.type import TaskExecutionDate
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_postpone_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    today = TaskExecutionDate(datetime.today())
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.postpone_task(todolist.name, task.to_key(), today)

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[task.having(execution_date=Some(today))]).to_snapshot()





