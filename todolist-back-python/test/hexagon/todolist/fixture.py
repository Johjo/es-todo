from expression import Option, Nothing, Some

from src.hexagon.shared.type import TaskKey, TodolistName
from src.hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from src.hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from test.fixture import TaskBuilder, TodolistBuilder


class TodolistSetForTest(TodolistSetPort):
    def __init__(self) -> None:
        self._all_snapshot: dict[TodolistName, Option[TodolistSnapshot]] = {}

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_snapshot:
            raise Exception(f"feed todolist '{todolist_name}' before getting tasks")
        return self._all_snapshot[todolist_name]

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._all_snapshot[todolist.name] = Some(todolist)

    def feed(self, todolist: TodolistBuilder):
        self._all_snapshot[todolist.to_name()] = Some(todolist.to_snapshot())

    def feed_nothing(self, todolist_name: str):
        self._all_snapshot[TodolistName(todolist_name)] = Nothing


class TaskKeyGeneratorForTest(TaskKeyGeneratorPort):
    def __init__(self) -> None:
        self.keys: list[TaskKey] | None = None

    def feed(self, *items: TaskKey | TaskSnapshot | TaskBuilder) -> None:
        self.keys = [self._key_from(item) for item in items]

    def generate(self) -> TaskKey:
        if not self.keys:
            raise Exception("key must be fed before generating")
        return self.keys.pop(0)

    @staticmethod
    def _key_from(item: TaskKey | TaskSnapshot | TaskBuilder):
        if isinstance(item, TaskSnapshot):
            return item.key
        if isinstance(item, TaskBuilder):
            return item.key

        return item
