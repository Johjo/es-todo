from peewee import Database  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from infra.peewee.sdk import PeeweeSdk


class TodolistPeewee(TodolistPort):
    def __init__(self, database: Database):
        self._database = database
        self._sdk = PeeweeSdk(database)

    def all_open_tasks(self, task_filter: WhichTaskFilter) -> list[Task]:
        all_tasks = self._sdk.all_open_tasks(task_filter.todolist_name)
        return [Task(id=task.key, name=task.name) for task in all_tasks if task_filter.include(task_name=task.name, task_date=task.execution_date)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistPeewee':
        return TodolistPeewee(dependencies.get_infrastructure(Database))

    @staticmethod
    def match_included_context(task_filter: WhichTaskFilter, task_name: str) -> bool:
        if task_filter.include_context == ():
            return True

        for context in task_filter.include_context:
            if any(context == word for word in task_name.split()):
                return True
        return False
