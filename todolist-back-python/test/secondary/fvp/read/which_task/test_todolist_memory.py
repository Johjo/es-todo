import pytest

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from infra.memory import Memory
from test.fixture import TodolistBuilder
from test.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TodolistMemory(TodolistPort):
    def __init__(self, memory: Memory):
        self.memory = memory

    def all_open_tasks(self, task_filter: WhichTaskFilter) -> list[Task]:
        tasks = [task for task in self.memory.all_tasks(todolist_name=task_filter.todolist_name) if task.is_open]
        return [Task(id=task.key, name=task.name) for task in tasks if task_filter.include(task.name)]

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistMemory':
        memory = dependencies.get_infrastructure(Memory)
        return TodolistMemory(memory)


class TestTodolistPeewee(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        self.memory.save(todolist.to_snapshot())

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        all_dependencies = Dependencies.create_empty()
        all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistMemory.factory)
        all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        return all_dependencies
