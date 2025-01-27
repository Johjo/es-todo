from collections import OrderedDict

from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.shared.type import TaskKey


class FvpMemory:
    def __init__(self) -> None:
        self._snapshot: FvpSnapshot = FvpSnapshot(OrderedDict[TaskKey, TaskKey]())

    def save(self, snapshot: FvpSnapshot):
        self._snapshot = snapshot

    def feed(self, snapshot: FvpSnapshot):
        self._snapshot = snapshot

    def by(self):
        return self._snapshot
