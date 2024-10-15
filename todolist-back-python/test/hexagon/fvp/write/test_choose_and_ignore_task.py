from typing import OrderedDict

import pytest

from test.fixture import an_id
from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from secondary.fvp.simple_session_repository import FvpSessionSetForTest


@pytest.fixture
def set_of_fvp_sessions():
    return FvpSessionSetForTest()


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


def test_should_save_snapshot(sut, set_of_fvp_sessions):
    sut.execute(chosen_task_id=1, ignored_task_id=2)
    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict[int, int]({an_id(2): an_id(1)}))


def test_should_load_snapshot(sut, set_of_fvp_sessions):
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[int, int]({an_id(2): an_id(1)})))

    sut.execute(chosen_task_id=1, ignored_task_id=3)

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[int, int]({an_id(2): an_id(1), an_id(3): an_id(1)}))


