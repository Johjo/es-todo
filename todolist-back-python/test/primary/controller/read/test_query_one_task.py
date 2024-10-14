from abc import ABC
from dataclasses import dataclass

from primary.controller.read.todolist import TodolistReadController, TodolistPort
from primary.controller.write.dependencies import Dependencies
from test.hexagon.todolist.fixture import TodolistFaker


@dataclass(frozen=True)
class Task:
    key: int
    name: str




class TodolistForTest(TodolistPort):
    def __init__(self) -> None:
        self._tasks: dict[(str, int,), Task] = {}

    def feed(self, todolist_name: str, task_key: int, task: Task):
        self._tasks[(todolist_name, task_key)] = task

    def task_by(self, todolist_name: str, task_key: int):
        assert (todolist_name, task_key) in self._tasks, "task must be fed before being read"
        return self._tasks[(todolist_name, task_key)]


def test_query_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = dependencies.feed_adapter(TodolistPort, lambda _: todolist)

    expected_task = Task(key=1, name="buy milk")
    todolist.feed(todolist_name="my todolist", task_key=1, task=expected_task)

    controller = TodolistReadController(dependencies)
    actual = controller.task_by("my todolist", expected_task.key)

    assert actual == expected_task


