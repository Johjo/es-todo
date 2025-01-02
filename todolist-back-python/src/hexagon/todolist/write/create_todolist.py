from expression import Result, Nothing, Error, Ok

from src.dependencies import Dependencies
from src.hexagon.shared.type import TodolistName
from src.hexagon.todolist.aggregate import TodolistAggregate
from src.hexagon.todolist.port import TodolistSetPort


class TodolistCreate:
    def __init__(self, todolist_set: TodolistSetPort) -> None:
        self._todolist_set: TodolistSetPort = todolist_set

    def execute(self, todolist_name: TodolistName) -> Result[None, None]:
        if self._todolist_set.by(todolist_name) != Nothing:
            return Error(None)

        self._todolist_set.save_snapshot(TodolistAggregate.create(todolist_name).to_snapshot())
        return Ok(None)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistCreate':
        return TodolistCreate(dependencies.get_adapter(TodolistSetPort))
