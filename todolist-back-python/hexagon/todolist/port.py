from abc import ABC, abstractmethod

from expression import Option

from hexagon.todolist.aggregate import TodolistSnapshot, TaskKey


class TodolistSetPort(ABC):
    @abstractmethod
    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        pass

    @abstractmethod
    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        pass


class TaskKeyGeneratorPort(ABC):
    @abstractmethod
    def generate(self) -> TaskKey:
        pass
