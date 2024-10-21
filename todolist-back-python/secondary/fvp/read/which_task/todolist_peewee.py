import re

from peewee import Database  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from secondary.todolist.table import Task as DbTask


class TodolistPeewee(TodolistPort):
    def __init__(self, database: Database):
        self._database = database

    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        with self._database.bind_ctx([DbTask]):
            all_tasks = DbTask.select().where(DbTask.todolist_name == task_filter.todolist_name, DbTask.is_open == True)
            return [Task(id=task.key, name=task.name) for task in all_tasks if self.filter(task, task_filter)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistPeewee':
        return TodolistPeewee(dependencies.get_infrastructure(Database))

    def filter(self, task: DbTask, task_filter: TaskFilter) -> bool:
        if not self.match_included_context(task_filter, task):
            return False

        if self.match_excluded_context(task_filter, task):
            return False

        return True

    @staticmethod
    def match_included_context(task_filter: TaskFilter, task: DbTask) -> bool:
        if task_filter.include_context == ():
            return True

        for context in task_filter.include_context:
            if any(context == word for word in task.name.split()):
                return True
        return False

    @staticmethod
    def match_excluded_context(task_filter: TaskFilter, task: DbTask) -> bool:
        for context in task_filter.exclude_context:
            if any(context == word for word in task.name.split()):
                return True
        return False
