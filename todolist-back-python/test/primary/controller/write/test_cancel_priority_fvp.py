from typing import OrderedDict

import pytest

from dependencies import Dependencies
from hexagon.fvp.type import TaskKey
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import a_task_key
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

    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(1): a_task_key(3)})))

    sut = TodolistWriteController(dependencies)
    sut.cancel_priority(a_task_key(3))

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)}))
