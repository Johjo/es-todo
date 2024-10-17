from typing import OrderedDict

import pytest

from dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import an_id
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from secondary.fvp.simple_session_repository import FvpSessionSetForTest


@pytest.fixture
def set_of_fvp_sessions():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


def test_should_choose_and_ignore_when_one_task_already_chosen(set_of_fvp_sessions, dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: set_of_fvp_sessions)

    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[int, int]({an_id(2): an_id(1)})))

    sut = TodolistWriteController(dependencies)
    sut.choose_and_ignore_task(chosen_task=1, ignored_task=3)

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[int, int]({an_id(2): an_id(1), an_id(3): an_id(1)}))
