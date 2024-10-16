from dataclasses import replace

from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_import_many_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    expected_tasks = [fake.a_task(1), fake.a_task(2)]
    todolist = replace(fake.a_todolist(), tasks=[])
    todolist_set.feed(todolist)

    sut.import_many_tasks(expected_tasks, todolist.name)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


