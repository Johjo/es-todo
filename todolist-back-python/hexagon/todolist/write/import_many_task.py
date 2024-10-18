from abc import ABC, abstractmethod
from dataclasses import dataclass

from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


@dataclass(frozen=True)
class TaskImported:
    name: str
    is_open: bool


class ExternalTodoListPort(ABC):
    @abstractmethod
    def all_tasks(self) -> list[TaskImported]:
        pass


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: str, external_todolist: ExternalTodoListPort):
        update = lambda todolist: todolist.import_tasks(external_todolist.all_tasks())
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)
