from src.hexagon.shared.type import TodolistKey
from src.infra.memory import Memory
from src.primary.todolist.read.port import AllTaskPort, AllTasksPresentation, TaskPresentation


class AllTaskInMemory(AllTaskPort):
    def __init__(self, memory: Memory):
        self._memory = memory

    def all_tasks(self, todolist_key: TodolistKey) -> AllTasksPresentation:
        all_tasks = self._memory.all_tasks(todolist_key=todolist_key, user_key=None)
        return AllTasksPresentation(tasks=[TaskPresentation(key=task.key, name=task.name, open=task.is_open, execution_date=task.execution_date.default_value(None)) for task in all_tasks])

