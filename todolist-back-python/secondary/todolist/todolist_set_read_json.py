import re
from datetime import date
from pathlib import Path
from uuid import UUID

from expression import Nothing, Some

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from infra.json_file import JsonFile
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadJson(TodolistSetReadPort):
    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        todolist = self._json_file.read(todolist_name).value
        return [self._to_task(task) for task in todolist["tasks"]]

    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist = self._json_file.read(todolist_name).value
        tasks = {UUID(task["key"]): task for task in todolist["tasks"]}
        task_data = tasks[task_key]
        return self._to_task(task_data)

    @staticmethod
    def _to_task(task):
        try:
            execution_date = Some(date.fromisoformat(task["execution_date"]))
        except TypeError:
            execution_date = Nothing

        return Task(id=TaskKey(UUID(task["key"])), name=task["name"], is_open=task["is_open"], execution_date=execution_date)

    def all_by_name(self) -> list[str]:
        return self._json_file.all_keys()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        todolist = self._json_file.read(todolist_name).value
        tasks = [self._to_task(task) for task in todolist["tasks"]]
        counts_by_context: dict[str, int] = {}
        for task in tasks:
            if task.is_open:
                contexts = self._extract_context_from_name(task)
                for context in contexts:
                    counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(context, count) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        return [TodolistContext(context.lower()) for context in contexts]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetReadJson':
        return TodolistSetReadJson(dependencies.get_path("todolist_json_path"))
