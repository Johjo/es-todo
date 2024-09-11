from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TaskAdded:
    title: str


class EventStore(ABC):
    @abstractmethod
    def store(self, event):
        pass


class AddTask:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def execute(self, title):
        self._event_store.store(TaskAdded(title=title))
