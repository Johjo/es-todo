import uuid
from pathlib import Path

from expression import Option

from dependencies import Dependencies
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from infra.json_file import JsonFile


class TodolistSetJson(TodolistSetPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._json_file.insert(todolist.name, self._to_todolist_dict(todolist))

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        todolist_as_dict = self._json_file.read(todolist_name)
        return todolist_as_dict.map(self._todolist_from_dict)

    def _to_todolist_dict(self, todolist: TodolistSnapshot):
        return {"name": todolist.name, "tasks": [self._to_task_dict(task) for task in todolist.tasks]}

    @staticmethod
    def _to_task_dict(task: TaskSnapshot):
        return {"key": str(task.key), "name": task.name, "is_open": task.is_open}

    def _todolist_from_dict(self, d):
        return TodolistSnapshot(name=d["name"], tasks=[self._task_from_dict(task) for task in d["tasks"]])

    @staticmethod
    def _task_from_dict(d):
        key = uuid.UUID(d["key"])
        return TaskSnapshot(name=d["name"], is_open=d["is_open"], key=key)

    @classmethod
    def factory(cls, dependencies: Dependencies):
        return TodolistSetJson(dependencies.get_path("todolist_json_path"))

