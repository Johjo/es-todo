from dataclasses import dataclass, replace
from uuid import UUID, uuid4

from faker import Faker

from hexagon.shared.type import TaskKey, TaskName, TodolistName, TaskOpen
from hexagon.todolist.aggregate import TaskSnapshot, TodolistSnapshot
from primary.controller.read.todolist import Task


def a_task_key(index: TaskKey | UUID | int | None = None) -> TaskKey:
    if isinstance(index, int):
        return TaskKey(UUID(int=index))
    if isinstance(index, UUID):
        return TaskKey(index)
    return TaskKey(uuid4())


@dataclass(frozen=True)
class TaskBuilder:
    key: TaskKey = None
    name: TaskName = None
    is_open: TaskOpen = None

    def to_snapshot(self) -> TaskSnapshot:
        if self.name is None:
            raise Exception("task.name must be set")
        if self.key is None:
            raise Exception("task.key must be set")
        if self.is_open is None:
            raise Exception("task.is_open must be set")

        return TaskSnapshot(key=TaskKey(self.key), name=TaskName(self.name), is_open=self.is_open)

    def having(self, **kwargs) -> 'TaskBuilder':
        return replace(self, **kwargs)

    def to_task(self) -> Task:
        return Task(id=self.key, name=self.name, is_open=self.is_open)


@dataclass(frozen=True)
class TodolistBuilder:
    name: TodolistName = None
    tasks: list[TaskBuilder] = None

    def having(self, **kwargs) -> 'TodolistBuilder':
        return replace(self, **kwargs)

    def to_snapshot(self) -> TodolistSnapshot:
        if self.name is None:
            raise Exception("todolist.name must be set")
        if self.tasks is None:
            raise Exception("todolist.tasks must be set")
        return TodolistSnapshot(name=TodolistName(self.name), tasks=[task.to_snapshot() for task in self.tasks])


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task_old(self, key: None | int | UUID = None) -> TaskSnapshot:
        return self.a_task(key).to_snapshot()

    def a_task(self, key: None | int | UUID = None) -> TaskBuilder:
        return TaskBuilder(key=self.task_key(key), name=self.task_name(), is_open=True)

    def a_todolist_old(self) -> TodolistSnapshot:
        return self.a_todolist().to_snapshot()

    def a_todolist(self, name: str | None = None) -> TodolistBuilder:
        if name is None:
            name = self.fake.word()
        return TodolistBuilder(name=name, tasks=[])

    @staticmethod
    def task_key(key: None | int | UUID | TaskKey = None) -> TaskKey:
        if key is None:
            return TaskKey(uuid4())
        if isinstance(key, int):
            return TaskKey(UUID(int=key))
        return TaskKey(key)

    def task_name(self) -> TaskName:
        return TaskName(self.fake.sentence())



