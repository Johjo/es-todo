import re
from typing import cast
from uuid import UUID

from expression import Option, Nothing, Some
from peewee import Database  # type: ignore

from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount, TaskKey, TaskName, TaskOpen, \
    TaskExecutionDate
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from infra.peewee.sdk import SqliteSdk
from infra.peewee.type import Task as TaskSdk, Todolist as TodolistSdk, TodolistDoesNotExist
from primary.controller.read.todolist import TodolistSetReadPort, TaskPresentation, TaskFilter
from shared.const import USER_KEY


def map_to_task_presentation(task: TaskSdk) -> TaskPresentation:
    return TaskPresentation(key=TaskKey(task.key),
                name=TaskName(task.name),
                is_open=TaskOpen(task.is_open),
                execution_date=task.execution_date.default_value(None))


class TodolistSetPeewee(TodolistSetPort):
    def __init__(self, database: Database, user_key: str):
        self._sdk = SqliteSdk(database)
        self._user_key = user_key


    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        try:
            todolist = self._sdk.todolist_by(user_key=self._user_key, todolist_name=todolist_name)
            tasks = self._sdk.all_tasks(user_key=self._user_key, todolist_name=todolist_name)
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
        self._sdk.upsert_todolist(user_key=self._user_key, todolist=TodolistSdk(name=todolist.name),
                                  tasks=[TaskSdk(key=task.key, name=task.name, is_open=task.is_open,
                                                 execution_date=task.execution_date) for task in todolist.tasks])

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetPeewee':
        return TodolistSetPeewee(database=dependencies.get_infrastructure(Database),
                                 user_key=dependencies.get_data(data_name=USER_KEY))


class TodolistSetReadPeewee(TodolistSetReadPort):
    def all_tasks_postponed_task(self, todolist_name: str):
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_tasks(user_key=self._user_key, todolist_name=todolist_name)
        all_tasks = [map_to_task_presentation(task) for task in all_tasks_sdk if
                     task.is_open and task.execution_date != Nothing]
        return sorted(all_tasks, key=lambda task: task.execution_date)

    def __init__(self, database: Database, user_key: str):
        self._user_key = user_key
        self._sdk = SqliteSdk(database)

    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_tasks(user_key=self._user_key, todolist_name=task_filter.todolist_name)
        return [map_to_task_presentation(task) for task in all_tasks_sdk if task_filter.include(task_name=task.name)]

    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        task: TaskSdk = self._sdk.task_by(todolist_name, task_key)
        return map_to_task_presentation(task)

    def all_by_name(self) -> list[TodolistName]:
        all_todolist: list[TodolistSdk] = self._sdk.all_todolist(user_key=self._user_key)
        return [TodolistName(todolist.name) for todolist in all_todolist]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_open_tasks(user_key=self._user_key, todolist_name=todolist_name)
        counts_by_context: dict[str, int] = {}
        for task in all_tasks_sdk:
            contexts = self._extract_context_from_name(task)
            for context in contexts:
                counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(TodolistContext(context), TodolistContextCount(count)) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        return [TodolistContext(context.lower()) for context in contexts]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetReadPeewee':
        return TodolistSetReadPeewee(database=dependencies.get_infrastructure(Database), user_key=dependencies.get_data(data_name=USER_KEY))
