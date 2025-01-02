from datetime import date

import pytest

from src.dependencies import Dependencies
from src.primary.controller.read.todolist import TodolistSetReadPort, TodolistReadController, TaskPresentation
from src.primary.controller.read.final_version_perfected import CalendarPort
from test.fixture import TodolistFaker, TaskBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class _TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._all_tasks: dict[str, list[TaskPresentation]] = {}

    def all_tasks_postponed_task(self, todolist_name: str) -> list[TaskPresentation]:
        return self._all_tasks[todolist_name]

    def feed(self, todolist_name: str, expected_tasks: list[TaskBuilder]):
        self._all_tasks[todolist_name] = [task.to_presentation() for task in expected_tasks]


@pytest.fixture
def todolist_set_read() -> _TodolistSetReadForTest:
    return _TodolistSetReadForTest()


class _CalendarForTest(CalendarPort):
    def __init__(self) -> None:
        self._today: date | None = None

    def today(self) -> date:
        if self._today is None:
            raise Exception("feed today date")
        return self._today

    def feed_today(self, today):
        self._today = today


@pytest.fixture
def calendar() -> _CalendarForTest:
    return _CalendarForTest()

@pytest.fixture
def dependencies(todolist_set_read: _TodolistSetReadForTest, calendar: _CalendarForTest) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set_read)
    dependencies = dependencies.feed_adapter(CalendarPort, lambda _: calendar)
    return dependencies

@pytest.fixture
def sut(dependencies: Dependencies) -> TodolistReadController:
    return TodolistReadController(dependencies)


def test_query_all_tasks(sut: TodolistReadController, todolist_set_read: _TodolistSetReadForTest, fake: TodolistFaker):
    # GIVEN
    expected_tasks = [fake.a_task(), fake.a_task()]
    todolist = fake.a_todolist()
    todolist_set_read.feed(todolist_name=todolist.to_name(), expected_tasks=expected_tasks)

    # WHEN
    actual = sut.all_tasks_postponed_task(todolist_name=todolist.to_name())

    # THEN
    assert actual == [task.to_presentation() for task in expected_tasks]
