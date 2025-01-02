from collections import OrderedDict
from uuid import uuid4

from test.fixture import a_task_key
from src.hexagon.fvp.write.reset_fvp_session import ResetFvpSession


from src.hexagon.fvp.aggregate import FvpSnapshot
from src.secondary.fvp.simple_session_repository import FvpSessionSetForTest


def test_reset_session():
    set_of_fvp_sessions = FvpSessionSetForTest()
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({a_task_key(1): 1, a_task_key(2): 0})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute()

    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict())
