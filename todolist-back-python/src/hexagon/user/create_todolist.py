from dataclasses import replace

from src.dependencies import Dependencies
from src.hexagon.shared.type import UserKey, TodolistName
from src.hexagon.user.port import UserRepositoryPort, TodolistUuidGeneratorPort, TodolistSnapshot, UserSnapshot


class CreateTodolist:
    def __init__(self, user_repository: UserRepositoryPort, todolist_uuid_generator: TodolistUuidGeneratorPort):
        self._todolist_uuid_generator = todolist_uuid_generator
        self._user_repository = user_repository

    def execute(self, user_key: UserKey, todolist_name: TodolistName) -> None:
        user = self._get_user_or_create_it(user_key)

        user = replace(user, todolist=(*user.todolist, TodolistSnapshot(
            key=self._todolist_uuid_generator.generate_todolist_key(), name=todolist_name)))

        self._save(user)

    def _save(self, user: UserSnapshot):
        self._user_repository.save(user)

    def _get_user_or_create_it(self, user_key: UserKey) -> UserSnapshot:
        user: UserSnapshot | None = self._user_repository.by_user(user_key)
        if user is None:
            return UserSnapshot(key=UserKey(user_key), todolist=())
        return user

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'CreateTodolist':
        return CreateTodolist(user_repository=dependencies.get_adapter(UserRepositoryPort),
                              todolist_uuid_generator=dependencies.get_adapter(TodolistUuidGeneratorPort))
