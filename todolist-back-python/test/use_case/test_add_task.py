import pytest

from use_case.add_task import EventStore, TaskAdded, AddTask


class EventStoreInMemory(EventStore):
    def __init__(self):
        self._events = []

    def store(self, event):
        self._events.append(event)


@pytest.mark.parametrize("title", ["buy milk", "buy eggs"])
def test_add_task(title):
    expected_event = TaskAdded(title=title)
    event_store = EventStoreInMemory()

    sut = AddTask(event_store)
    sut.execute(expected_event.title)

    assert event_store._events == [expected_event]
