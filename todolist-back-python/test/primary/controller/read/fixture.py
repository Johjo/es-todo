from datetime import date

from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import TodolistSetReadPort, TaskPresentation, TaskFilter


class TodolistSetReadPortNotImplemented(TodolistSetReadPort):
    def all_tasks_postponed_task(self, todolist_name: str, reference_date: date):
        ...

    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        raise NotImplementedError()

    def all_by_name(self) -> list[TodolistName]:
        raise NotImplementedError()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()

    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        raise NotImplementedError()


