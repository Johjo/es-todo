import re
from typing import cast

from expression import Option, Nothing, Some
from peewee import Database  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TaskFilter
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount, TaskKey, TaskName, TaskOpen, \
    TaskExecutionDate
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from infra.peewee.sdk import PeeweeSdk, Task as TaskSdk, Todolist as TodolistSdk, TodolistDoesNotExist
from primary.controller.read.todolist import TodolistSetReadPort, Task


def map_to_task_presentation(task: TaskSdk) -> Task:
    return Task(id=TaskKey(task.key),
                name=TaskName(task.name),
                is_open=TaskOpen(task.is_open),
                execution_date=cast(Option[TaskExecutionDate], task.execution_date))


class TodolistSetPeewee(TodolistSetPort, TodolistSetReadPort):
    def __init__(self, database: Database):
        self._sdk = PeeweeSdk(database)

    # todo task_filter
    def all_tasks(self, todolist_name: TodolistName, task_filter: TaskFilter) -> list[Task]:
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_tasks(todolist_name=task_filter.todolist_name)
        return [map_to_task_presentation(task) for task in all_tasks_sdk if task_filter.include(task_name=task.name)]

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        task: TaskSdk = self._sdk.task_by(todolist_name, task_key)
        return map_to_task_presentation(task)

    def all_by_name(self) -> list[TodolistName]:
        all_todolist : list[TodolistSdk] = self._sdk.all_todolist()
        return [TodolistName(todolist.name) for todolist in all_todolist]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_open_tasks(todolist_name=todolist_name)
        counts_by_context: dict[str, int]= {}
        for task in all_tasks_sdk:
            contexts = self._extract_context_from_name(task)
            for context in contexts:
                counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(TodolistContext(context), TodolistContextCount(count)) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        return [TodolistContext(context.lower()) for context in contexts]

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        try:
            todolist = self._sdk.todolist_by(todolist_name=todolist_name)
            tasks = self._sdk.all_tasks(todolist_name)
            return Some(self._to_todolist_snapshot(todolist, tasks))
        except TodolistDoesNotExist:
            return Nothing

    def _to_todolist_snapshot(self, todolist: TodolistSdk, tasks: list[TaskSdk]) -> TodolistSnapshot:
        return TodolistSnapshot(name=TodolistName(todolist.name),
                                tasks=tuple([self._to_task_snapshot(task) for task in tasks]))

    @staticmethod
    def _to_task_snapshot(task: TaskSdk) -> TaskSnapshot:
        return TaskSnapshot(key=TaskKey(task.key), name=TaskName(task.name), is_open=TaskOpen(task.is_open),
                            execution_date=cast(Option[TaskExecutionDate], task.execution_date))

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._sdk.upsert_todolist(todolist=TodolistSdk(name=todolist.name),
                                  tasks=[TaskSdk(key=task.key, name=task.name, is_open=task.is_open,
                                                 execution_date=task.execution_date) for task in todolist.tasks])

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetPeewee':
        return TodolistSetPeewee(dependencies.get_infrastructure(Database))