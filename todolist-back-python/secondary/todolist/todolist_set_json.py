import uuid
from datetime import date
from pathlib import Path

from expression import Option, Nothing, Some

from dependencies import Dependencies
from hexagon.shared.type import TaskKey
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
        return {"key": str(task.key), "name": task.name, "is_open": task.is_open, "execution_date": task.execution_date.map(lambda d: d.isoformat()).default_value(None)}

    def _todolist_from_dict(self, d):
        return TodolistSnapshot(name=d["name"], tasks=tuple(self._task_from_dict(task) for task in d["tasks"]))

    @staticmethod
    def _task_from_dict(d):
        key = uuid.UUID(d["key"])
        try:
            execution_date = Some(date.fromisoformat(d["execution_date"]))
        except TypeError:
            execution_date = Nothing
        return TaskSnapshot(key=TaskKey(key), name=d["name"], is_open=d["is_open"], execution_date=execution_date)

    @classmethod
    def factory(cls, dependencies: Dependencies):
        return TodolistSetJson(dependencies.get_path("todolist_json_path"))

