from expression import Option, Nothing, Some
from faker import Faker

from hexagon.todolist.aggregate import TodolistSnapshot, TodolistSetPort, TaskKey, TaskSnapshot


def a_todolist_snapshot(name: str) -> TodolistSnapshot:
    return TodolistSnapshot(name=name, tasks=[])


class TodolistSetForTest(TodolistSetPort):
    def __init__(self) -> None:
        self._all_snapshot: dict[str, TodolistSnapshot] = {}

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self._all_snapshot[snapshot.name] = snapshot

    def history(self):
        return [name for name in self._all_snapshot]

    def feed(self, snapshot: TodolistSnapshot):
        self._all_snapshot[snapshot.name] = snapshot

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_snapshot:
            return Nothing
        return Some(self._all_snapshot[todolist_name])


def a_task_key(value: int):
    return TaskKey(value=value)


def a_task(key: int, faker: Faker):
    return TaskSnapshot(key=a_task_key(key), name=faker.sentence())


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task(self, key: None | int = None) -> TaskSnapshot:
        if key is None:
            key = self.fake.random_int()
        return TaskSnapshot(key=TaskKey(key), name=self.fake.sentence(), is_open=True)

    def a_todolist(self) -> TodolistSnapshot:
        return TodolistSnapshot(name=self.fake.word(), tasks=[])
