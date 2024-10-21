from pathlib import Path
from uuid import UUID

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from infra.json_file import JsonFile
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadJson(TodolistSetReadPort):
    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        raise NotImplementedError()

    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist = self._json_file.read(todolist_name).value
        tasks = {UUID(task["key"]): task for task in todolist["tasks"]}
        task = tasks[task_key]
        return Task(id=TaskKey(UUID(task["key"])), name=task["name"], is_open=task["is_open"])

    def all_by_name(self) -> list[str]:
        return self._json_file.all_keys()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetReadJson':
        return TodolistSetReadJson(dependencies.get_path("todolist_json_path"))
