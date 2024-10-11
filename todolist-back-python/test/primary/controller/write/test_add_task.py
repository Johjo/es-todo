# step 1 : copy use case test
# step 2 : remove fixture
# step 3 : introduce dependencies
# step 4 : pass adapter from dependencies
# step 5 : create use case factory from dependencies
# step 6 : feed dependencies with use case factory
# step 7 : create controller
# step 8 : extract method using use case
# step 9 : move method to controller




from dataclasses import replace

import pytest
from faker import Faker

from hexagon.todolist.aggregate import TodolistSetPort
from hexagon.todolist.write.open_task import OpenTask
from primary.controller.write.create_todolist import TodolistWriteController
from primary.controller.write.dependencies import Dependencies
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)


def test_open_task_when_no_task(dependencies_with_use_cases, fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)

    dependencies = dependencies_with_use_cases.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    expected_task = fake.a_task()

    todolist_name = todolist.name
    task_key = expected_task.key
    task_name = expected_task.name

    controller = TodolistWriteController(dependencies)
    controller.open_task(dependencies, task_key, task_name, todolist_name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])




