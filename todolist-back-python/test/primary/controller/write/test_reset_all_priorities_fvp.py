from typing import OrderedDict

import pytest
from faker.proxy import Faker

from dependencies import Dependencies
from hexagon.shared.type import TaskKey
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from secondary.fvp.simple_session_repository import FvpSessionSetForTest


@pytest.fixture
def set_of_fvp_sessions():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


@pytest.fixture
def fake():
    return TodolistFaker(Faker())


def test_reset_all_priorities(set_of_fvp_sessions, fake: TodolistFaker, dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: set_of_fvp_sessions)

    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[TaskKey, TaskKey]({fake.a_task(2).key: fake.a_task(1).key, fake.a_task(1).key: fake.a_task(3).key})))

    sut = TodolistWriteController(dependencies)
    sut.reset_all_priorities()

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]())
