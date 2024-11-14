from hexagon.fvp.read.which_task import TaskFilter
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadPortNotImplemented(TodolistSetReadPort):
    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        raise NotImplementedError()

    def all_by_name(self) -> list[TodolistName]:
        raise NotImplementedError()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()

    # todo task_filter
    def all_tasks(self, todolist_name: TodolistName, task_filter: TaskFilter) -> list[Task]:
        raise NotImplementedError()
