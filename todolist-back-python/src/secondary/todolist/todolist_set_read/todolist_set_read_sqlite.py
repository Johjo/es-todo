import re
import sqlite3

from expression import Nothing

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskKey, TaskName, TaskOpen, TodolistName, TodolistContext, TodolistContextCount
from src.infra.sqlite.sdk import SqliteSdk
from src.infra.sqlite.type import Task as TaskSdk, Todolist as TodolistSdk
from src.primary.controller.read.todolist import TaskPresentation, TodolistSetReadPort, TaskFilter
from src.shared.const import USER_KEY


def map_to_task_presentation(task: TaskSdk) -> TaskPresentation:
    return TaskPresentation(key=TaskKey(task.key),
                name=TaskName(task.name),
                is_open=TaskOpen(task.is_open),
                execution_date=task.execution_date.default_value(None))


class TodolistSetReadSqlite(TodolistSetReadPort):
    def all_tasks_postponed_task(self, todolist_name: str):
        all_tasks_sdk: list[TaskSdk] = self._sdk.all_tasks(user_key=self._user_key, todolist_name=todolist_name)
        all_tasks = [map_to_task_presentation(task) for task in all_tasks_sdk if
                     task.is_open and task.execution_date != Nothing]
        return sorted(all_tasks, key=lambda task: task.execution_date)

    def __init__(self, connection: sqlite3.Connection, user_key: str):
        self._user_key = user_key
        self._sdk = SqliteSdk(connection)

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
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetReadSqlite':
        return TodolistSetReadSqlite(connection=dependencies.get_infrastructure(sqlite3.Connection),
                                     user_key=dependencies.get_data(data_name=USER_KEY))
