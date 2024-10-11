from abc import ABC
from collections import namedtuple
from dataclasses import dataclass, replace, field
from typing import Any

from hexagon.todolist.aggregate import TodolistSetPort
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.open_task import OpenTask


@dataclass(frozen=True)
class Dependencies(ABC):
    use_case_factory: dict[Any, Any] = field(default_factory=dict)
    adapter_factory: Any = None

    def get_adapter(self, port) -> Any:
        assert self.adapter_factory, f"adapter for {port} must be injected first"
        return self.adapter_factory(self)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return replace(self, use_case_factory={**self.use_case_factory, use_case: use_case_factory})


    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return replace(self, adapter_factory=adapter_factory)

    def get_use_case(self, use_case: Any) -> Any:
        assert use_case in self.use_case_factory, f"use_case for {use_case} must be injected first"
        return self.use_case_factory[use_case](self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    factories = {
        TodolistCreate: todolist_create_factory,
        OpenTask : open_task_use_case_factory,
    }

    for use_case, factory in factories.items():
        dependencies = dependencies.feed_use_case(use_case, factory)
    return dependencies


def todolist_create_factory(dependencies: Dependencies):
    return TodolistCreate(dependencies.get_adapter(TodolistSetPort))

def open_task_use_case_factory(dependencies: Dependencies):
    return OpenTask(dependencies.get_adapter(TodolistSetPort))
