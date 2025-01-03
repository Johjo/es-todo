from datetime import timedelta

from expression import Some

from src.primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import DateTimeProviderForTest
from test.primary.controller.write.conftest import TodolistSetForTest


def test_postpone_task(todolist_set: TodolistSetForTest, datetime_provider: DateTimeProviderForTest, sut: TodolistWriteController, fake: TodolistFaker):
    today = fake.a_datetime()
    tomorrow = today + timedelta(days=1)
    datetime_provider.feed(today)

    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.postpone_task_to_tomorrow(todolist.name, task.to_key())

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[task.having(execution_date=Some(tomorrow.date()))]).to_snapshot()





