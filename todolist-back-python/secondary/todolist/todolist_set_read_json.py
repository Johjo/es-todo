from pathlib import Path

from infra.json_file import JsonFile
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadJson(TodolistSetReadPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def task_by(self, todolist_name: str, task_key: int) -> Task:
        todolist = self._json_file.read(todolist_name)
        tasks = {task["key"]: task for task in todolist["tasks"]}
        task = tasks[task_key]
        return Task(id=task["key"], name=task["name"])

    def all_by_name(self) -> list[str]:
        return self._json_file.all_keys()
