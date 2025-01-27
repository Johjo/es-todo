from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.infra.fvp_memory import FvpMemory


class FvpSessionSetInMemory(FvpSessionSetPort):
    def __init__(self, fvp_memory: FvpMemory) -> None:
        self._memory = fvp_memory

    def save(self, snapshot: FvpSnapshot) -> None:
        self._memory.save(snapshot)

    def by(self) -> FvpSnapshot:
        return self._memory.by()

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'FvpSessionSetInMemory':
        return FvpSessionSetInMemory(fvp_memory=(dependencies.get_infrastructure(FvpMemory)))
