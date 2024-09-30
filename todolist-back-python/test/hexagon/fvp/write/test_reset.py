from collections import OrderedDict
from uuid import uuid4

from fixture import an_id
from hexagon.fvp.write.reset_fvp_session import ResetFvpSession


from hexagon.fvp.domain_model import FvpSnapshot
from secondary.fvp.simple_session_repository import SimpleSessionRepository


def test_reset_session():
    set_of_fvp_sessions = SimpleSessionRepository()
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({an_id(1): 1, an_id(2): 0})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute()

    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict())
