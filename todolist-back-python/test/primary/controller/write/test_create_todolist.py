from dataclasses import dataclass, replace

import pytest
from mock import MagicMock
from abc import ABC, abstractmethod
from typing import Any

from hexagon.todolist.aggregate import TodolistSetPort
from hexagon.todolist.write.create_todolist import TodolistCreate
from test.hexagon.todolist.fixture import TodolistSetForTest


@dataclass(frozen=True)
class Dependencies(ABC):
    use_case_factory: Any = None
    adapter_factory: Any = None

    def get_adapter(self, port) -> Any:
        assert self.adapter_factory, f"adapter for {port} must be injected first"
        return self.adapter_factory(self)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return replace(self, use_case_factory=use_case_factory)

    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return replace(self, adapter_factory=adapter_factory)

    def get_use_case(self, use_case_name: Any) -> Any:
        assert self.use_case_factory, f"use_case for {use_case_name} must be injected first"
        return self.use_case_factory(self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()


class TodolistController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    def create_todolist(self, todolist_name):
        todolist_create = self.dependencies.get_use_case(TodolistCreate)
        todolist_create.execute(todolist_name=todolist_name)


@pytest.fixture
def empty_dependencies():
    return Dependencies.create_empty()


@pytest.fixture
def dependencies_with_use_cases():
    return inject_use_cases(Dependencies.create_empty())


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    return dependencies.feed_use_case(TodolistCreate, todolist_create_factory)


def todolist_create_factory(dependencies: Dependencies):
    return TodolistCreate(dependencies.get_adapter(TodolistSetPort))


@pytest.mark.parametrize("todolist_name", ["my_todolist", "my_todolist2"])
def test_use_case(empty_dependencies, todolist_name: str):
    use_case = MagicMock()
    dependencies = empty_dependencies.feed_use_case(TodolistCreate, lambda d: use_case)

    TodolistController(dependencies).create_todolist(todolist_name)

    use_case.execute.assert_called_once_with(todolist_name=todolist_name)


def test_create_todolist(dependencies_with_use_cases):
    todolist_set = TodolistSetForTest()
    dependencies = dependencies_with_use_cases.feed_adapter(TodolistSetPort, lambda _: todolist_set)

    TodolistController(dependencies).create_todolist("my_todolist")

    assert todolist_set.by("my_todolist").value.name == "my_todolist"

# def test_create_todolist():
#     todolist_set = TodolistSetForTest()
#     dependencies = DependenciesForTest()
#     dependencies.feed_adapter(TodolistSetPort, todolist_set)
#     controller = TodoListController(dependencies)
#     controller.create_todolist()
#
#     todolist_set = dependencies.get_adapter(TodolistSetPort)
#     assert todolist_set.by("my_todolist").value.name == "my_todolist"
#
