from typing import Tuple

from hexagon.shared.type import TaskKey, TaskOpen, TaskName
from primary.controller.read.todolist import TodolistReadController, TodolistSetReadPort, Task
from dependencies import Dependencies
from test.fixture import a_task_key, TodolistFaker
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


# todo: don't use this in web test
class TodolistForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._tasks: dict[Tuple[str, TaskKey,], Task] = {}

    # todo get id from task
    def feed(self, todolist_name: str, task_key: TaskKey, task: Task):
        self._tasks[(todolist_name, task_key)] = task

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        assert self.already_fed(task_key, todolist_name), "task must be fed before being read"
        return self._tasks[(todolist_name, task_key)]

    def already_fed(self, task_key, todolist_name):
        return (todolist_name, task_key) in self._tasks


def test_query_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist)

    expected_task = fake.a_task(1).having(name=TaskName("buy milk"), is_open=TaskOpen(True)).to_task()
    todolist.feed(todolist_name="my todolist", task_key=a_task_key(1), task=expected_task)

    controller = TodolistReadController(dependencies)
    actual = controller.task_by("my todolist", expected_task.id)

    assert actual == expected_task
