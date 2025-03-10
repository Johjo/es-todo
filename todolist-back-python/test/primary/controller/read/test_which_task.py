from dataclasses import replace
from datetime import date

import pytest
from faker import Faker

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import DoTheTask, FvpSnapshot, FvpSessionSetPort
from src.hexagon.fvp.read.which_task import TodolistPort
from src.hexagon.shared.type import UserKey
from src.infra.fvp_memory import FvpMemory
from src.primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController, CalendarPort
from test.hexagon.fvp.read.test_which_task import TodolistForTest, FvpFaker


@pytest.fixture
def todolist():
    return TodolistForTest()


@pytest.fixture
def fvp_session_set(dependencies: Dependencies) -> FvpSessionSetPort:
    return dependencies.get_adapter(FvpSessionSetPort)


@pytest.fixture
def fake() -> FvpFaker:
    return FvpFaker(Faker())


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


def test_which_task_when_two_and_one_chosen(dependencies: Dependencies, todolist: TodolistForTest,
                                            fvp_memory: FvpMemory, calendar: _CalendarForTest,
                                            fake: FvpFaker, faker: Faker):
    # GIVEN
    ignored_task = replace(fake.a_task(2))
    chosen_task = replace(fake.a_task(1))
    reference_date = faker.date_object()
    calendar.feed_today(reference_date)
    task_filter = replace(fake.a_which_task_filter(), reference_date=reference_date)

    user_key = UserKey("the user")
    fvp_memory.feed(user_key=user_key, snapshot=FvpSnapshot.from_primitive_dict({ignored_task.key: chosen_task.key}))
    todolist.feed(user_key, task_filter, chosen_task, ignored_task)

    dependencies = dependencies.feed_adapter(TodolistPort, lambda _: todolist)
    dependencies = dependencies.feed_adapter(CalendarPort, lambda _: calendar)

    # WHEN
    actual = FinalVersionPerfectedReadController(dependencies).which_task(user_key=user_key,
                                                                          todolist_name=task_filter.todolist_name,
                                                                          include_context=task_filter.include_context,
                                                                          exclude_context=task_filter.exclude_context,
                                                                          task_filter=task_filter)

    # THEN
    assert actual == DoTheTask(key=chosen_task.key)
