from abc import ABC, abstractmethod

from expression import Option

from hexagon.shared.type import TaskKey, TodolistName
from hexagon.todolist.aggregate import TodolistSnapshot


class TodolistSetPort(ABC):
    @abstractmethod
    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        pass

    @abstractmethod
    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        pass


class TaskKeyGeneratorPort(ABC):
    @abstractmethod
    def generate(self) -> TaskKey:
        pass
