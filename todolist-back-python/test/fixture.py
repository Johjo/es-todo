from dataclasses import dataclass, replace
from uuid import UUID, uuid4

from faker import Faker

from hexagon.shared.type import TaskKey, TaskName, TodolistName
from hexagon.todolist.aggregate import TaskSnapshot, TodolistSnapshot


def a_task_key(index: TaskKey | UUID | int | None = None) -> TaskKey:
    if isinstance(index, int):
        return TaskKey(UUID(int=index))
    if isinstance(index, UUID):
        return TaskKey(index)
    return TaskKey(uuid4())


@dataclass(frozen=True)
class TaskBuilder:
    key: UUID | None = None
    name: str | None = None
    is_open: bool | None = None

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


@dataclass(frozen=True)
class TodolistBuilder:
    name: str | None = None
    tasks: list[TaskBuilder] | None = None

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
        if key is None:
            key = uuid4()
        if isinstance(key, int):
            key = UUID(int=key)
        return TaskBuilder(key=key, name=self.fake.sentence(), is_open=True).to_snapshot()

    def a_todolist_old(self) -> TodolistSnapshot:
        return TodolistBuilder(name=self.fake.word(), tasks=[]).to_snapshot()
