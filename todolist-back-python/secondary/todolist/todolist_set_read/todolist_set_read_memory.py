import re

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from infra.memory import Memory
from primary.controller.read.todolist import TodolistSetReadPort, Task


class TodolistSetReadInMemory(TodolistSetReadPort):
    def __init__(self, memory: Memory):
        self.memory = memory

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        task = self.memory.task_by(todolist_name, task_key)
        return Task(id=task.key, name=task.name, is_open=task.is_open, execution_date=task.execution_date)

    def all_by_name(self) -> list[TodolistName]:
        return [TodolistName(name) for name in self.memory.all_todolist_by_name()]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        tasks = [Task(id=task.key, name=task.name, is_open=task.is_open, execution_date=task.execution_date) for task in self.memory.all_tasks(todolist_name)]
        counts_by_context: dict[str, int] = {}
        for task in tasks:
            if task.is_open:
                contexts = self._extract_context_from_name(task)
                for context in contexts:
                    counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(TodolistContext(context), TodolistContextCount(count)) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        return [TodolistContext(context.lower()) for context in contexts]


    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        return [Task(id=task.key, name=task.name, is_open=task.is_open, execution_date=task.execution_date) for task in self.memory.all_tasks(todolist_name)]

    @classmethod
    def factory(cls, dependencies: Dependencies)-> 'TodolistSetReadInMemory':
        memory = dependencies.get_infrastructure(Memory)
        return TodolistSetReadInMemory(memory)
