from collections import OrderedDict
from uuid import uuid4, UUID

from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from test.hexagon.fvp.test_double import SimpleFvpSessionRepository

from hexagon.fvp.domain_model import FvpSnapshot


def a_task_id(index: int | None = None):
    if index:
        return UUID(int=index, version=4)
    return uuid4()


def test_reset_session():
    set_of_fvp_sessions = SimpleFvpSessionRepository()
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({a_task_id(1): 1, a_task_id(2): 0})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute()

    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict())
