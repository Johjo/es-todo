from collections import OrderedDict

from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.shared.type import TaskKey


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
