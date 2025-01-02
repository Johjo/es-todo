import sqlite3

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import Task
from src.hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from src.infra.sqlite.sdk import SqliteSdk
from src.shared.const import USER_KEY


class TodolistSqlite(TodolistPort):
    def __init__(self, connection: sqlite3.Connection, user_key: str):
        self._sdk = SqliteSdk(connection)
        self._user_key = user_key

    def all_open_tasks(self, task_filter: WhichTaskFilter) -> list[Task]:
        all_tasks = self._sdk.all_open_tasks(user_key=self._user_key, todolist_name=task_filter.todolist_name)
        return [Task(key=task.key) for task in all_tasks if task_filter.include(task_name=task.name, task_date=task.execution_date)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSqlite':
        return TodolistSqlite(connection=dependencies.get_infrastructure(sqlite3.Connection),
                              user_key=dependencies.get_data(USER_KEY))

