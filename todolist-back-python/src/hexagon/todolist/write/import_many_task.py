from abc import ABC, abstractmethod
from dataclasses import dataclass

from expression import Result, Nothing

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskKey, TaskName, TaskOpen
from src.hexagon.todolist.aggregate import TodolistAggregate, TaskSnapshot
from src.hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from src.hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


@dataclass(frozen=True)
class TaskImported:
    name: TaskName
    is_open: TaskOpen

    def to_snapshot(self, key: TaskKey) -> TaskSnapshot:
        return TaskSnapshot(key=key, name=self.name, is_open=self.is_open, execution_date=Nothing)


class ExternalTodoListPort(ABC):
    @abstractmethod
    def all_tasks(self) -> list[TaskImported]:
        pass


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort, task_key_generator: TaskKeyGeneratorPort):
        self._todolist_set = todolist_set
        self._task_key_generator = task_key_generator

    def execute(self, todolist_name: str, external_todolist: ExternalTodoListPort):
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.import_tasks([task.to_snapshot(self._task_key_generator.generate()) for task in external_todolist.all_tasks()])

        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'ImportManyTask':
        return ImportManyTask(dependencies.get_adapter(TodolistSetPort), dependencies.get_adapter(TaskKeyGeneratorPort))