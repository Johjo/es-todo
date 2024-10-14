from abc import ABC
from dataclasses import dataclass, replace, field
from typing import Any

from hexagon.fvp.port import FvpSessionSetPort
from hexagon.fvp.read.which_task import WhichTaskQuery, TodolistPort
from hexagon.todolist.aggregate import TodolistSetPort
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTask, TaskKeyGeneratorPort
from hexagon.todolist.write.reword_task import RewordTask


@dataclass(frozen=True)
class Dependencies(ABC):
    use_case_factory: dict[Any, Any] = field(default_factory=dict)
    adapter_factory: dict[Any, Any] = field(default_factory=dict)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return replace(self, use_case_factory={**self.use_case_factory, use_case: use_case_factory})

    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return replace(self, adapter_factory={**self.adapter_factory, port: adapter_factory})

    def get_use_case(self, use_case: Any) -> Any:
        assert use_case in self.use_case_factory, f"use_case for {use_case} must be injected first"
        return self.use_case_factory[use_case](self)

    def get_query(self, query: Any) -> Any:
        return self.get_use_case(query)

    def get_adapter(self, port) -> Any:
        assert port in self.adapter_factory, f"adapter for {port} must be injected first"
        return self.adapter_factory[port](self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    factories = {
        TodolistCreate: todolist_create_factory,
        OpenTask: open_task_use_case_factory,
        CloseTask: close_task_use_case_factory,
        RewordTask: reword_task_use_case_factory,
        ImportManyTask: import_many_task_use_case_factory,
        WhichTaskQuery: which_task_query_factory
    }

    for use_case, factory in factories.items():
        dependencies = dependencies.feed_use_case(use_case, factory)
    return dependencies


def todolist_create_factory(dependencies: Dependencies):
    return TodolistCreate(dependencies.get_adapter(TodolistSetPort))


def open_task_use_case_factory(dependencies: Dependencies):
    todolist_set = dependencies.get_adapter(TodolistSetPort)
    task_key_generator = dependencies.get_adapter(TaskKeyGeneratorPort)
    return OpenTask(todolist_set, task_key_generator)


def close_task_use_case_factory(dependencies):
    return CloseTask(dependencies.get_adapter(TodolistSetPort))


def reword_task_use_case_factory(dependencies: Dependencies) -> RewordTask:
    return RewordTask(dependencies.get_adapter(TodolistSetPort))


def import_many_task_use_case_factory(dependencies: Dependencies) -> ImportManyTask:
    return ImportManyTask(dependencies.get_adapter(TodolistSetPort))

def which_task_query_factory(dependencies: Dependencies) -> WhichTaskQuery:
    return WhichTaskQuery(dependencies.get_adapter(TodolistPort), dependencies.get_adapter(FvpSessionSetPort))
