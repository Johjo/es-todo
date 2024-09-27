from typing import OrderedDict
from uuid import uuid4

import pytest

from test.fixture import an_id
from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from secondary.fvp.simple_session_repository import SimpleSessionRepository


@pytest.fixture
def set_of_fvp_sessions():
    return SimpleSessionRepository()


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


def test_should_save_snapshot(sut, set_of_fvp_sessions):
    chosen_task_id = an_id(1)
    ignored_task_id = an_id(2)

    sut.execute(chosen_task_id, ignored_task_id)

    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict[uuid4, int]({an_id(1): 1, an_id(2): 0}))


def test_should_load_snapshot(sut, set_of_fvp_sessions):
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({an_id(1): 1, an_id(2): 0})))

    chosen_task_id = an_id(1)
    ignored_task_id = an_id(3)

    sut.execute(chosen_task_id, ignored_task_id)

    assert set_of_fvp_sessions.by() == FvpSnapshot(
        OrderedDict[uuid4, int]({an_id(1): 1, an_id(2): 0, an_id(3): 0}))


