import re

from expression import Nothing

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from src.infra.memory import Memory
from src.primary.controller.read.todolist import TodolistSetReadPort, TaskPresentation, TaskFilter
from src.shared.const import USER_KEY


class TodolistSetReadInMemory(TodolistSetReadPort):
    def __init__(self, memory: Memory, user_key: str):
        self._user_key = user_key
        self.memory = memory

    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        task = self.memory.task_by(user_key=self._user_key, todolist_name=todolist_name, task_key=task_key)
        return self._to_task_presentation(task)

    @staticmethod
    def _to_task_presentation(task):
        return TaskPresentation(key=task.key, name=task.name, is_open=task.is_open,
                                execution_date=task.execution_date.default_value(None))

    def all_by_name(self) -> list[TodolistName]:
        return sorted([TodolistName(name) for name in self.memory.all_todolist_by_name(user_key=self._user_key)])

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        tasks = self.memory.all_tasks(user_key=self._user_key, todolist_name=todolist_name)
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

    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        return [self._to_task_presentation(task) for task in self.memory.all_tasks(user_key=self._user_key, todolist_name=task_filter.todolist_name) if task_filter.include(task_name=task.name)]

    def all_tasks_postponed_task(self, todolist_name: str):
        tasks = [self._to_task_presentation(task) for task in self.memory.all_tasks(user_key=self._user_key, todolist_name=todolist_name) if
                    task.is_open and task.execution_date != Nothing]
        return sorted(tasks, key=lambda task: task.execution_date)

    @classmethod
    def factory(cls, dependencies: Dependencies)-> 'TodolistSetReadInMemory':
        memory = dependencies.get_infrastructure(Memory)
        return TodolistSetReadInMemory(memory=memory, user_key=dependencies.get_data(data_name=USER_KEY))









