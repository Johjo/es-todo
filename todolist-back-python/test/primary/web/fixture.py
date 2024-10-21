from typing import Any

from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import Task
from test.fixture import TodolistBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class CleanResponse:
    def __init__(self, response: Any) :
        self._response = response

    def location(self) -> str:
        full_location = self._response.headers['Location']
        without_protocol = full_location.split("//")[1]
        without_localhost = without_protocol.split("/", 1)[1]
        return "/" + without_localhost


class TodolistSetForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self.tasks_by_todolist: dict[TodolistName, list[Task]] = {}

    def feed(self, todolist: TodolistBuilder) -> None:
        self.tasks_by_todolist[todolist.name] = [task.to_task() for task in todolist.tasks]

    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        if todolist_name not in self.tasks_by_todolist:
            raise Exception(f"feed todolist '{todolist_name}' before getting tasks")
        return self.tasks_by_todolist[todolist_name]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        return [(TodolistContext("#context_1"), TodolistContextCount(5)),
                (TodolistContext("#context_2"), TodolistContextCount(10)), ]
