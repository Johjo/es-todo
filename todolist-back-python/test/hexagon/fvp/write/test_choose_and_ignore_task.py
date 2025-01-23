from typing import OrderedDict

import pytest

from src.hexagon.shared.type import TaskKey
from test.fixture import a_task_key
from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory


@pytest.fixture
def fvp_sessions_set():
    return FvpSessionSetInMemory()


@pytest.fixture
def sut(fvp_sessions_set):
    return ChooseAndIgnoreTaskFvp(fvp_sessions_set)


def test_should_choose_and_ignore_when_no_task_already_chosen(sut, fvp_sessions_set):
    sut.execute(chosen_task_id=a_task_key(1), ignored_task_id=a_task_key(2))
    assert fvp_sessions_set.by() == FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)}))


def test_should_choose_and_ignore_when_one_task_already_chosen(sut, fvp_sessions_set):
    fvp_sessions_set.feed(FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)})))

    sut.execute(chosen_task_id=a_task_key(1), ignored_task_id=a_task_key(3))

    assert fvp_sessions_set.by() == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(3): a_task_key(1)}))


