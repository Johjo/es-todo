from dataclasses import replace

from primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_reword_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    task = fake.a_task_old()
    todolist = replace(fake.a_todolist_old(), tasks=[task])
    todolist_set.feed(todolist)

    sut.reword_task(todolist.name, task.key, "buy the milk")

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[(replace(task, name="buy the milk"))])




