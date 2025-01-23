from typing import OrderedDict

import pytest
from faker.proxy import Faker

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from src.hexagon.shared.type import TaskKey
from src.primary.controller.write.todolist import TodolistWriteController
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory
from test.fixture import TodolistFaker


@pytest.fixture
def set_of_fvp_sessions():
    return FvpSessionSetInMemory()


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


@pytest.fixture
def fake():
    return TodolistFaker(Faker())


def test_reset_all_priorities(set_of_fvp_sessions, fake: TodolistFaker, dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: set_of_fvp_sessions)

    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[TaskKey, TaskKey](
        {fake.a_task(2).to_key(): fake.a_task(1).to_key(),
         fake.a_task(1).to_key(): fake.a_task(3).to_key()})))

    sut = TodolistWriteController(dependencies)
    sut.reset_all_priorities()

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]())
