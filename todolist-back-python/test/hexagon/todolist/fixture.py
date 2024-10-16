from expression import Option, Nothing, Some
from faker import Faker

from hexagon.todolist.aggregate import TodolistSnapshot, TaskKey, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from primary.controller.read.todolist import TodolistSetReadPort, Task


def a_todolist_snapshot(name: str) -> TodolistSnapshot:
    return TodolistSnapshot(name=name, tasks=[])


class TodolistSetForTest(TodolistSetPort, TodolistSetReadPort):
    def task_by(self, todolist_name: str, task_key: int) -> Task:
        raise Exception("Not implemented")

    def __init__(self) -> None:
        self._all_snapshot: dict[str, TodolistSnapshot] = {}

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self._all_snapshot[snapshot.name] = snapshot

    def history(self):
        return [name for name in self._all_snapshot]

    def feed(self, *snapshots: TodolistSnapshot):
        for snapshot in snapshots:
            self._all_snapshot[snapshot.name] = snapshot

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_snapshot:
            return Nothing
        return Some(self._all_snapshot[todolist_name])

    def all_by_name(self) -> list[str]:
        return [snapshot.name for snapshot in self._all_snapshot.values()]


def a_task_key(value: int):
    return TaskKey(value=value)


def a_task(key: int, faker: Faker) -> TaskSnapshot:
    return TaskSnapshot(key=a_task_key(key), name=faker.sentence(), is_open=True)


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task(self, key: None | int = None) -> TaskSnapshot:
        if key is None:
            key = self.fake.random_int()
        return TaskSnapshot(key=TaskKey(key), name=self.fake.sentence(), is_open=True)

    def a_todolist(self) -> TodolistSnapshot:
        return TodolistSnapshot(name=self.fake.word(), tasks=[])
