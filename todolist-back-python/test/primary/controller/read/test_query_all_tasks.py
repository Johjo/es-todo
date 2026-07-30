import pytest

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort, TodolistReadController, TaskPresentation, \
    TaskFilter
from test.fixture import TodolistFaker, TaskFilterBuilder, TaskBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class _TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._all_tasks: dict[TaskFilter, list[TaskPresentation]] = {}

    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        if task_filter not in self._all_tasks:
            raise Exception("Feed task for task filter")
        return self._all_tasks[task_filter]

    def feed(self, task_filter: TaskFilterBuilder, expected_tasks: list[TaskBuilder]):
        self._all_tasks[task_filter.build()] = [task.to_presentation() for task in expected_tasks]


@pytest.fixture
def todolist_set_read() -> _TodolistSetReadForTest:
    return _TodolistSetReadForTest()

@pytest.fixture
def dependencies(todolist_set_read: _TodolistSetReadForTest) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set_read)
    return dependencies

@pytest.fixture
def sut(dependencies: Dependencies) -> TodolistReadController:
    return TodolistReadController(dependencies)


def test_query_all_tasks(sut: TodolistReadController, todolist_set_read: _TodolistSetReadForTest, dependencies: Dependencies, fake: TodolistFaker):
    # GIVEN
    expected_tasks = [fake.a_task(), fake.a_task()]
    task_filter = fake.a_task_filter(todolist_name=fake.a_todolist().to_name())
    todolist_set_read.feed(task_filter, expected_tasks)

    # WHEN
    actual = sut.all_task(task_filter.build())

    # THEN
    assert actual == [task.to_presentation() for task in expected_tasks]
