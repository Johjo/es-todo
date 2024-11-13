from dataclasses import replace

from primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_close_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[task])
    todolist_set.feed(todolist)

    sut.close_task(todolist_name=todolist.name, task_key=task.key)

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[(replace(task, is_open=False))]).to_snapshot()
