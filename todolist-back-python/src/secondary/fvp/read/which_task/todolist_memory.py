from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import Task
from src.hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from src.infra.memory import Memory
from src.shared.const import USER_KEY


class TodolistMemory(TodolistPort):
    def __init__(self, memory: Memory, user_key:str):
        self.memory = memory
        self._user_key = user_key

    def all_open_tasks(self, task_filter: WhichTaskFilter) -> list[Task]:
        tasks = [task for task in self.memory.all_tasks(user_key=self._user_key, todolist_name=task_filter.todolist_name) if task.is_open]
        return [Task(key=task.key) for task in tasks if
                task_filter.include(task.name, task.execution_date)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistMemory':
        memory = dependencies.get_infrastructure(Memory)
        return TodolistMemory(memory=memory, user_key=dependencies.get_data(USER_KEY))
