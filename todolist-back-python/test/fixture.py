from dataclasses import dataclass, replace
from datetime import datetime
from uuid import UUID, uuid4

from expression import Option, Nothing, Some
from faker import Faker

from hexagon.shared.type import TaskKey, TaskName, TodolistName, TaskOpen, TaskExecutionDate
from hexagon.todolist.aggregate import TaskSnapshot, TodolistSnapshot
from infra.peewee import sdk
from primary.controller.read.todolist import Task





def a_task_key(index: TaskKey | UUID | int | None = None) -> TaskKey:
    if isinstance(index, int):
        return TaskKey(UUID(int=index))
    if isinstance(index, UUID):
        return TaskKey(index)
    return TaskKey(uuid4())


@dataclass(frozen=True)
class TaskBuilder:
    key: TaskKey | UUID | None = None
    name: TaskName | str | None = None
    is_open: TaskOpen | bool | None= None
    execution_date: Option[TaskExecutionDate | datetime] | TaskExecutionDate | datetime | None = None

    def having(self, **kwargs) -> 'TaskBuilder':
        return replace(self, **kwargs)

    def to_snapshot(self) -> TaskSnapshot:
        return TaskSnapshot(key=self.to_key(), name=self.to_name(), is_open=self.to_open(), execution_date=self.to_execution_date())

    def to_task(self) -> Task:
        return Task(id=self.to_key(), name=self.to_name(), is_open=self.to_open(), execution_date=self.to_execution_date())

    def to_key(self) -> TaskKey:
        if self.key is None:
            raise Exception("task.key must be set")
        return TaskKey(self.key)

    def to_name(self) -> TaskName:
        if self.name is None:
            raise Exception("task.name must be set")
        return TaskName(self.name)

    def to_open(self) -> TaskOpen:
        if self.is_open is None:
            raise Exception("task.is_open must be set")
        return TaskOpen(self.is_open)

    def to_execution_date(self) -> Option[TaskExecutionDate] :
        if self.execution_date is None:
            raise Exception("task.execution_date must be set")
        if self.execution_date == Nothing:
            return Nothing
        if isinstance(self.execution_date, datetime):
            return Some(TaskExecutionDate(self.execution_date))
        if isinstance(self.execution_date, Option):
            return self.execution_date
        return Some(TaskExecutionDate(self.execution_date))

    def to_peewee_sdk(self) -> sdk.Task:
        return sdk.Task(key=self.to_key(), name=self.to_name(), is_open=self.to_open())


@dataclass(frozen=True)
class TodolistBuilder:
    name: TodolistName = TodolistName("undefined")
    tasks: list[TaskBuilder] | None= None

    def having(self, **kwargs) -> 'TodolistBuilder':
        return replace(self, **kwargs)

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(name=self.to_name(), tasks=tuple(task.to_snapshot() for task in self.to_tasks()))

    def to_tasks(self) -> list[TaskBuilder]:
        if self.tasks is None:
            raise Exception("todolist.tasks must be set")
        return self.tasks

    def to_name(self) -> TodolistName:
        if self.name == "undefined":
            raise Exception("todolist.name must be set")
        return TodolistName(self.name)

    def to_peewee_sdk(self) -> sdk.Todolist:
        return sdk.Todolist(name=self.to_name())


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task(self, key: None | int | UUID = None) -> TaskBuilder:
        return TaskBuilder(key=self.task_key(key), name=self.task_name(), is_open=True, execution_date=Nothing)

    def a_closed_task(self, key: None | int | UUID = None) -> TaskBuilder:
        return self.a_task(key).having(is_open=False)

    def a_todolist(self, name: TodolistName | str | None = None) -> TodolistBuilder:
        if name is None:
            name = self.fake.word()
        return TodolistBuilder(name=TodolistName(name), tasks=[])

    @staticmethod
    def task_key(key: None | int | UUID | TaskKey = None) -> TaskKey:
        if key is None:
            return TaskKey(uuid4())
        if isinstance(key, int):
            return TaskKey(UUID(int=key))
        return TaskKey(key)

    def task_name(self) -> TaskName:
        return TaskName(self.fake.sentence())



