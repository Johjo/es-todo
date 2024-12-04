from expression import Result, pipe

from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TaskKey, TaskExecutionDate
from hexagon.todolist.aggregate import TodolistAggregate, TodolistSnapshot
from hexagon.todolist.port import TodolistSetPort


class TodolistRepository:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def load_aggregate(self, todolist_name: TodolistName) -> Result[TodolistAggregate, str]:
        return pipe(todolist_name, self._load_snapshot, self._from_snapshot)

    def save_aggregate(self, aggregate: Result[TodolistAggregate, str]) -> Result[None, str]:
        return pipe(aggregate,
                    self.to_snapshot,
                    self._save_snapshot)

    @staticmethod
    def _from_snapshot(snapshot: Result[TodolistSnapshot, str]) -> Result[TodolistAggregate, str]:
        return snapshot.map(TodolistAggregate.from_snapshot)

    def _load_snapshot(self, todolist_name: TodolistName) -> Result[TodolistSnapshot, str]:
        return self._todolist_set.by(todolist_name).to_result(error="todolist not found")

    @staticmethod
    def to_snapshot(todolist: Result[TodolistAggregate, str]) -> Result[TodolistSnapshot, str]:
        return todolist.map(lambda t: t.to_snapshot())

    def _save_snapshot(self, snapshot: Result[TodolistSnapshot, str]) -> Result[None, str]:
        return snapshot.map(self._todolist_set.save_snapshot)


class PostPoneTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: TodolistName, key: TaskKey, execution_date: TaskExecutionDate):
        def update(todolist: Result[TodolistAggregate, str]) -> Result[TodolistAggregate, str]:
            return todolist.bind(lambda t: t.postpone_task(key, execution_date))

        repository = TodolistRepository(self._todolist_set)

        return pipe(todolist_name,
                    repository.load_aggregate,
                    update,
                    repository.save_aggregate)

    @staticmethod
    def factory(dependencies: Dependencies) -> 'PostPoneTask':
        todolist_set = dependencies.get_adapter(TodolistSetPort)
        return PostPoneTask(todolist_set)
