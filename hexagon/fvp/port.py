from abc import ABC, abstractmethod

from hexagon.fvp.domain_model import FvpSnapshot


class FvpSessionRepository(ABC):
    @abstractmethod
    def save(self, snapshot: FvpSnapshot) -> None:
        pass

    @abstractmethod
    def by(self) -> FvpSnapshot | None:
        pass
