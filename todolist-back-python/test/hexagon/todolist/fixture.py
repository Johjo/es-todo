from expression import Option, Nothing, Some

from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from primary.controller.read.todolist import TodolistSetReadPort, Task


def a_todolist_snapshot_old(name: str) -> TodolistSnapshot:
    return TodolistSnapshot(name=name, tasks=[])


class TodolistSetForTest(TodolistSetPort, TodolistSetReadPort):
    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
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


class TaskKeyGeneratorForTest(TaskKeyGeneratorPort):
    def __init__(self) -> None:
        self.keys: list[TaskKey] | None = None

    def feed(self, *items: TaskKey | TaskSnapshot) -> None:
        self.keys = [self._key_from(item) for item in items]

    def generate(self) -> TaskKey:
        if not self.keys:
            raise Exception("key must be fed before generating")
        return self.keys.pop(0)

    @staticmethod
    def _key_from(item: TaskKey | TaskSnapshot):
        if isinstance(item, TaskSnapshot):
            return item.key
        return item
