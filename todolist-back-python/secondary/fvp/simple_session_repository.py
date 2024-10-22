from collections import OrderedDict

from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class FvpSessionSetForTest(FvpSessionSetPort):
    def __init__(self) -> None:
        self.snapshot: FvpSnapshot | None = None

    def save(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot

    def by(self) -> FvpSnapshot | None:
        if self.snapshot is None:
            return FvpSnapshot(OrderedDict[int, int]())
        return self.snapshot

    def feed(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot
