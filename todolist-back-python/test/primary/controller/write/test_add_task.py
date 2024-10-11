from dataclasses import replace

import pytest
from faker import Faker

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


def test_open_task_when_no_task(dependencies_with_use_cases, fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    dependencies = dependencies_with_use_cases.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    expected_task = fake.a_task()

    controller = TodolistWriteController(dependencies)
    controller.open_task(todolist_name=todolist.name,
                         task_key=expected_task.key.value,
                         task_name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])
