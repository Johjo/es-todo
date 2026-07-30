from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.shared.type import UserKey
from infra.fvp_memory import FvpMemory
from shared.const import USER_KEY


class FvpSessionSetInMemory(FvpSessionSetPort):
    def __init__(self, fvp_memory: FvpMemory) -> None:
        self._memory = fvp_memory

    def save(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        self._memory.save(user_key=user_key, snapshot=snapshot)

    def by(self, user_key: UserKey) -> FvpSnapshot:
        return self._memory.by(user_key=user_key)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'FvpSessionSetInMemory':
        fvp_memory = dependencies.get_infrastructure(FvpMemory)
        return FvpSessionSetInMemory(fvp_memory=fvp_memory)
