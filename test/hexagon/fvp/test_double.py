from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionRepository


class SimpleFvpSessionRepository(FvpSessionRepository):
    def __init__(self):
        self.snapshot = None

    def save(self, snapshot: FvpSnapshot) -> None:
        self.snapshot = snapshot

    def by(self) -> FvpSnapshot:
        return self.snapshot

    def feed(self, snapshot: FvpSnapshot):
        self.snapshot = snapshot
