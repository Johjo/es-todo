from pathlib import Path

from expression import Option, Some

from dependencies import Dependencies
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot, TaskKey
from hexagon.todolist.port import TodolistSetPort
from infra.json_file import JsonFile


class TodolistSetJson(TodolistSetPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._json_file.insert(todolist.name, self._to_todolist_dict(todolist))

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        todolist_as_dict = self._json_file.read(todolist_name)
        return Some(self._todolist_from_dict(todolist_as_dict))

    def _to_todolist_dict(self, todolist: TodolistSnapshot):
        return {"name": todolist.name, "tasks": [self._to_task_dict(task) for task in todolist.tasks]}

    @staticmethod
    def _to_task_dict(task: TaskSnapshot):
        return {"key": task.key.value, "name": task.name, "is_open": task.is_open}

    def _todolist_from_dict(self, d):
        return TodolistSnapshot(name=d["name"], tasks=[self._task_from_dict(task) for task in d["tasks"]])

    @staticmethod
    def _task_from_dict(d):
        return TaskSnapshot(key=TaskKey(d["key"]), name=d["name"], is_open=d["is_open"])

    @classmethod
    def factory(cls, dependencies: Dependencies):
        return TodolistSetJson(dependencies.get_path("todolist_json_path"))

