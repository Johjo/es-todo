from abc import ABC, abstractmethod
from dataclasses import dataclass

from expression import Result, Nothing, Error, Ok, Option


@dataclass
class TodolistSnapshot:
    name: str


class TodolistAggregate:
    def __init__(self, name: str) -> None:
        self._name = name

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(self._name)


class TodolistSetPort(ABC):
    @abstractmethod
    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        pass

    def save(self, snapshot: TodolistSnapshot) -> None:
        pass


class TodolistCreate:
    def __init__(self, todolist_set: TodolistSetPort) -> None:
        self._todolist_set: TodolistSetPort = todolist_set

    def execute(self, todolist_name: str) -> Result[None, None]:
        if self._todolist_set.by(todolist_name) != Nothing:
            return Error(None)

        self._todolist_set.save(TodolistAggregate(todolist_name).to_snapshot())
        return Ok(None)
