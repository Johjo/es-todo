from collections import OrderedDict

from src.hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot
from src.hexagon.shared.type import TaskKey


class FvpSessionSetForTest(FvpSessionSetPort):
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
