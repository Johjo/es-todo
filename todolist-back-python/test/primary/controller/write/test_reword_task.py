from dataclasses import replace

from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_reword_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    task = fake.a_task()
    todolist = replace(fake.a_todolist(), tasks=[task])
    todolist_set.feed(todolist)

    sut.reword_task(todolist.name, task.key.value,"buy the milk")

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[(replace(task, name="buy the milk"))])




