from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from expression import Option

@dataclass(frozen=True)
class TaskKey:
    value: int


@dataclass
class TaskSnapshot:
    key: TaskKey
    name: str

@dataclass
class TodolistSnapshot:
    name: str
    tasks : list[TaskSnapshot]


@dataclass(frozen=True)
class Task:
    key: TaskKey
    name: str

    def to_snapshot(self) -> TaskSnapshot:
        return TaskSnapshot(key=self.key, name=self.name)

    @classmethod
    def from_snapshot(cls, snapshot) -> 'Task':
        return Task(key=snapshot.key, name=snapshot.name)


@dataclass(frozen=True)
class TodolistAggregate:
    name: str
    tasks: tuple[Task, ...]

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(self.name, tasks=[task.to_snapshot() for task in self.tasks])

    @classmethod
    def from_snapshot(cls, snapshot: TodolistSnapshot) -> 'TodolistAggregate':
        return TodolistAggregate(name=snapshot.name, tasks=(*[Task.from_snapshot(task) for task in snapshot.tasks], ))

    def open_task(self, task: Task) -> 'TodolistAggregate':
        return TodolistAggregate(name=self.name, tasks=self.tasks + (task,))

    @classmethod
    def create(cls, todolist_name) -> 'TodolistAggregate':
        return TodolistAggregate(name=todolist_name, tasks=())


class TodolistSetPort(ABC):
    @abstractmethod
    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        pass

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        pass
