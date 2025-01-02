from typing import Tuple

from src.hexagon.shared.type import TaskKey
from src.primary.controller.read.todolist import TodolistReadController, TodolistSetReadPort, TaskPresentation
from src.dependencies import Dependencies
from test.fixture import TodolistFaker, TaskBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._tasks: dict[Tuple[str, TaskKey,], TaskPresentation] = {}

    def feed(self, todolist_name: str, task: TaskBuilder):
        self._tasks[(todolist_name, task.to_key())] = task.to_presentation()

    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        assert self.already_fed(task_key, todolist_name), "task must be fed before being read"
        return self._tasks[(todolist_name, task_key)]

    def already_fed(self, task_key, todolist_name):
        return (todolist_name, task_key) in self._tasks


def test_query_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist = TodolistSetReadForTest()
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist)

    expected_task = fake.a_task()
    todolist.feed(todolist_name="my todolist", task=expected_task)

    controller = TodolistReadController(dependencies)
    actual = controller.task_by("my todolist", expected_task.to_key())

    assert actual == expected_task.to_presentation()
