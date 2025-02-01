from src.dependencies import Dependencies
from src.hexagon.shared.type import UserKey
from src.hexagon.user.port import UserRepositoryPort, UserSnapshot


class UserRepositoryInMemory(UserRepositoryPort):
    def __init__(self) -> None:
        self.user : dict[UserKey, UserSnapshot] = {}

    def save(self, user: UserSnapshot) -> None:
        self.user[user.key] = user

    def by_user(self, key: UserKey) -> UserSnapshot | None:
        if key not in self.user:
            return None
        return self.user[key]

    @classmethod
    def factory(cls, _: Dependencies) -> 'UserRepositoryInMemory':
        return UserRepositoryInMemory()
