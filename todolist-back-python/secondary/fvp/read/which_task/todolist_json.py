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
        return self._to_task_list(todolist.value)

    @staticmethod
    def _to_task_list(todolist: dict[Any, Any]) -> list[Task]:
        return [Task(id=TaskKey(UUID(task["key"])), name=task["name"]) for task in todolist["tasks"] if task["is_open"] == True]

    @classmethod
    def factory(cls, dependencies: Dependencies):
        json_path = dependencies.get_path("todolist_json_path")
        return TodolistJson(json_path)
