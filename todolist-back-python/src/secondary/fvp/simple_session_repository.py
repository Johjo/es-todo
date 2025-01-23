from collections import OrderedDict

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.hexagon.shared.type import TaskKey


class FvpSessionSetInMemory(FvpSessionSetPort):
    def __init__(self) -> None:
        self.snapshot: FvpSnapshot | None = None

    def save(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot

    def by(self) -> FvpSnapshot:
        if self.snapshot is None:
            return FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        return self.snapshot

    def feed(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'FvpSessionSetInMemory':
        return FvpSessionSetInMemory()
