from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import cast

from expression import Option

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount, TaskOpen, TaskName, \
    TaskExecutionDate


# todo : use a task key instead of an id
@dataclass
class Task:
    id: TaskKey
    name: TaskName
    is_open: TaskOpen
    execution_date: Option[TaskExecutionDate]


# todo : use TaskPresentation instead Task
class TodolistSetReadPort(ABC):
    @abstractmethod
    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        pass

    @abstractmethod
    def all_by_name(self) -> list[TodolistName]:
        pass

    @abstractmethod
    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        pass

    @abstractmethod
    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        pass


class TodolistReadController:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def all_todolist_by_name(self) -> list[str]:
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return cast(list[str], todolist_set.all_by_name())

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return todolist_set.task_by(todolist_name=todolist_name, task_key=task_key)

    def counts_by_context(self, todolist_name: str):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        context = todolist_set.counts_by_context(todolist_name=TodolistName(todolist_name))
        return sorted(context)

    def to_markdown(self, todolist_name: str):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return to_markdown(todolist_set.all_tasks(TodolistName(todolist_name)))


def to_markdown(tasks: list[Task]) -> str:
    def task_to_markdown(task: Task) -> str:
        return f"- [{" " if task.is_open else "x"}] {task.name}"
    return "\n".join([task_to_markdown(task) for task in tasks])
