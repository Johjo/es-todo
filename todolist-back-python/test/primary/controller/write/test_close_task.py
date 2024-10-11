from dataclasses import replace

import pytest
from faker import Faker

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_close_task(dependencies_with_use_cases: Dependencies, fake: TodolistFaker):
    task = fake.a_task()
    todolist = replace(fake.a_todolist(), tasks=[task])
    todolist_set = TodolistSetForTest()
    todolist_set.feed(todolist)

    dependencies = dependencies_with_use_cases.feed_adapter(TodolistSetPort, lambda _: todolist_set)

    controller = TodolistWriteController(dependencies)
    controller.close_task(todolist_name=todolist.name, task_key=task.key.value)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[(replace(task, is_open=False))])
