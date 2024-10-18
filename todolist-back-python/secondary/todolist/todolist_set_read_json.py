from pathlib import Path
from uuid import UUID

from dependencies import Dependencies
from hexagon.fvp.type import TaskKey
from infra.json_file import JsonFile
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadJson(TodolistSetReadPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist = self._json_file.read(todolist_name).value
        tasks = {UUID(task["key"]): task for task in todolist["tasks"]}
        task = tasks[task_key]
        return Task(id=UUID(task["key"]), name=task["name"])

    def all_by_name(self) -> list[str]:
        return self._json_file.all_keys()

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetReadJson':
        return TodolistSetReadJson(dependencies.get_path("todolist_json_path"))
