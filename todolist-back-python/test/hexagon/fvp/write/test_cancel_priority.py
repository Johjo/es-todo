import pytest

from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.fvp.write.cancel_priority import CancelPriorityFvp
from test.fixture import a_task_key
from test.hexagon.fvp.write.fixture import FvpSessionSetForTest


@pytest.fixture
def session_set():
    return FvpSessionSetForTest()

@pytest.fixture
def sut(session_set: FvpSessionSetForTest):
    return CancelPriorityFvp(session_set)

def test_remove_priority_when_only_one(sut: CancelPriorityFvp, session_set: FvpSessionSetForTest):
    session_set.feed(FvpSnapshot.from_primitive_dict({a_task_key(2): a_task_key(1)}))

    sut.execute(a_task_key(1))

    assert session_set.by() == FvpSnapshot.from_primitive_dict({})


def test_cancel_priority_when_one_task(sut: CancelPriorityFvp, session_set: FvpSessionSetForTest):
    session_set.feed(FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2), a_task_key(2): a_task_key(3)}))

    sut.execute(a_task_key(3))

    assert session_set.by() == FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2)})

def test_cancel_priority_when_many_links(sut: CancelPriorityFvp, session_set: FvpSessionSetForTest):
    session_set.feed(FvpSnapshot.from_primitive_dict({a_task_key(1): a_task_key(2), a_task_key(3): a_task_key(2)}))

    sut.execute(a_task_key(2))

    assert session_set.by() == FvpSnapshot.from_primitive_dict({})
