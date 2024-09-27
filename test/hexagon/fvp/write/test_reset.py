from collections import OrderedDict
from uuid import uuid4

from fixture import an_id
from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from test.hexagon.fvp.test_double import SimpleFvpSessionRepository

from hexagon.fvp.domain_model import FvpSnapshot


def test_reset_session():
    set_of_fvp_sessions = SimpleFvpSessionRepository()
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({an_id(1): 1, an_id(2): 0})))
    sut = ResetFvpSession(set_of_fvp_sessions)
    sut.execute()

    assert set_of_fvp_sessions.by() == FvpSnapshot(OrderedDict())
