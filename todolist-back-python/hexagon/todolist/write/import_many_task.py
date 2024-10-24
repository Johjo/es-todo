from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from expression import Result

from dependencies import Dependencies
from hexagon.shared.type import TaskKey
from hexagon.todolist.aggregate import TodolistAggregate, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


@dataclass(frozen=True)
class TaskImported:
    name: str
    is_open: bool

    def to_snapshot(self, key: TaskKey) -> TaskSnapshot:
        return TaskSnapshot(key=key, name=self.name, is_open=self.is_open)


class ExternalTodoListPort(ABC):
    @abstractmethod
    def all_tasks(self) -> list[TaskImported]:
        pass


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort, task_key_generator: TaskKeyGeneratorPort):
        self._external_todolist: ExternalTodoListPort | None = None
        self._todolist_set = todolist_set
        self._task_key_generator = task_key_generator

    def execute(self, todolist_name: str, external_todolist: ExternalTodoListPort):
        self._external_todolist = external_todolist
        update = lambda todolist: todolist.import_tasks(external_todolist.all_tasks())
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, self._update)

    def _update(self, todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
        return todolist.import_tasks([task.to_snapshot(self._task_key_generator.generate()) for task in self._external_todolist.all_tasks()])

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'ImportManyTask':
        return ImportManyTask(dependencies.get_adapter(TodolistSetPort), dependencies.get_adapter(TaskKeyGeneratorPort))