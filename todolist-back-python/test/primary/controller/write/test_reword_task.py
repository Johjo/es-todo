from dataclasses import replace

from hexagon.todolist.aggregate import TaskKey
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.reword_task import RewordTask
from primary.controller.dependencies import Dependencies, reword_task_use_case_factory
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


def test_reword_task(dependencies: Dependencies, fake: TodolistFaker):
    task = fake.a_task()
    todolist_set = TodolistSetForTest()
    todolist = replace(fake.a_todolist(), tasks=[task])
    todolist_set.feed(todolist)

    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    controller = TodolistWriteController(dependencies)
    controller.reword_task(todolist.name, task.key.value,"buy the milk")

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=[(replace(task, name="buy the milk"))])




