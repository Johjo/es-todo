from pathlib import Path
from typing import Any
from uuid import UUID

from expression import Nothing

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from hexagon.shared.type import TaskKey
from infra.json_file import JsonFile


class TodolistJson(TodolistPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        todolist = self._json_file.read(task_filter.todolist_name)
        if todolist is Nothing:
            return []
        tasks = self._to_task_list(todolist.value)
        return [task for task in tasks if self.filter(task, task_filter)]

    def filter(self, task: Task, task_filter: TaskFilter) -> bool:
        if not self.match_included_context(task_filter, task):
            return False

        if self.match_excluded_context(task_filter, task):
            return False

        return True

    @staticmethod
    def match_included_context(task_filter: TaskFilter, task: Task) -> bool:
        if task_filter.include_context == ():
            return True

        for context in task_filter.include_context:
            if any(context == word for word in task.name.split()):
                return True
        return False

    @staticmethod
    def match_excluded_context(task_filter: TaskFilter, task: Task) -> bool:
        for context in task_filter.exclude_context:
            if any(context == word for word in task.name.split()):
                return True
        return False



    @staticmethod
    def _to_task_list(todolist: dict[Any, Any]) -> list[Task]:
        return [Task(id=TaskKey(UUID(task["key"])), name=task["name"]) for task in todolist["tasks"] if task["is_open"]]

    @classmethod
    def factory(cls, dependencies: Dependencies):
        json_path = dependencies.get_path("todolist_json_path")
        return TodolistJson(json_path)
