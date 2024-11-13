from expression import Option, Nothing, Some

from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from primary.controller.read.todolist import TodolistSetReadPort, Task
from test.fixture import TaskBuilder, TodolistBuilder


class TodolistSetForTest(TodolistSetPort, TodolistSetReadPort):
    def __init__(self) -> None:
        self._all_snapshot: dict[str, TodolistSnapshot] = {}

    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        raise NotImplementedError()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        todolist = self._all_snapshot[todolist_name]
        task_snapshot = next(task for task in todolist.tasks if task.key == task_key)
        return Task(name=task_snapshot.name, id=task_snapshot.key, is_open=task_snapshot.is_open,
                    execution_date=task_snapshot.execution_date)

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self._all_snapshot[snapshot.name] = snapshot

    def history(self):
        return [name for name in self._all_snapshot]

    def feed(self, *all_todolist: TodolistBuilder):
        for todolist in all_todolist:
            if isinstance(todolist, TodolistSnapshot):
                self._all_snapshot[todolist.name] = todolist
            if isinstance(todolist, TodolistBuilder):
                self._all_snapshot[todolist.name] = todolist.to_snapshot()

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_snapshot:
            return Nothing
        return Some(self._all_snapshot[todolist_name])

    def all_by_name(self) -> list[TodolistName]:
        return [snapshot.name for snapshot in self._all_snapshot.values()]


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
