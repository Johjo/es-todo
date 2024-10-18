from abc import ABC, abstractmethod
from dataclasses import dataclass

from dependencies import Dependencies
from hexagon.fvp.type import TaskKey


# todo : use a task key instead of an id
@dataclass
class Task:
    id: TaskKey
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }



class TodolistSetReadPort(ABC):
    @abstractmethod
    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        pass

    @abstractmethod
    def all_by_name(self) -> list[str]:
        pass



class TodolistReadController:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def all_todolist_by_name(self) -> list[str]:
        todolist_set : TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return todolist_set.all_by_name()

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist_set : TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return todolist_set.task_by(todolist_name=todolist_name, task_key=task_key)

class TodolistRead:
    class Port:
        Todolist = TodolistSetReadPort