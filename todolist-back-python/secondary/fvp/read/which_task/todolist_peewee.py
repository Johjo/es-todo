from peewee import Database

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from secondary.todolist.table import Task as DbTask


class TodolistPeewee(TodolistPort):
    def __init__(self, database: Database):
        self._database = database

    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        with self._database.bind_ctx([DbTask]):
            return [Task(id=task.key, name=task.name) for task in DbTask.select().where(DbTask.todolist_name == task_filter.todolist_name, DbTask.is_open==True)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistPeewee':
        return TodolistPeewee(dependencies.get_infrastructure(Database))
