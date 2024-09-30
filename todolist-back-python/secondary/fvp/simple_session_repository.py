from collections import OrderedDict
from uuid import UUID

from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionRepository
from utils import SharedInstanceBuiltIn


class SimpleSessionRepository(FvpSessionRepository, SharedInstanceBuiltIn):
    def __init__(self) -> None:
        self.snapshot: FvpSnapshot | None = None

    def save(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot

    def by(self) -> FvpSnapshot | None:
        if self.snapshot is None:
            return FvpSnapshot(OrderedDict[UUID, int]())
        return self.snapshot

    def feed(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot
