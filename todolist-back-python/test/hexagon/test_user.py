# créer une todolist pour un utilisateur
# que se passe-t-il si la todolist existe déjà ?
# que se passe-t-il si le user n'existe pas ?
# est-ce qu'on peut créer une todolist pour deux users ?
# est-ce qu'on gère l'uuid ?
from dataclasses import dataclass, replace
from typing import Tuple
from uuid import UUID, uuid4

import pytest

from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName


@dataclass(frozen=True)
class TodolistSnapshot:
    key: TodolistKey
    name: TodolistName


@dataclass(frozen=True)
class UserSnapshot:
    key: UserKey
    todolist: Tuple[TodolistSnapshot, ...]


class TodolistUuidGeneratorForTest:
    def __init__(self) -> None:
        self._next_uuid: UUID | None = None

    def feed(self, next_uuid: UUID) -> None:
        self._next_uuid = next_uuid

    def generate_todolist_key(self) -> TodolistKey:
        if self._next_uuid is None:
            raise Exception("feed next_uuid before generating todolist key")
        return TodolistKey(self._next_uuid)


class UserRepositoryForTest:
    def __init__(self) -> None:
        self._snapshot: UserSnapshot | None = None

    def save(self, snapshot: UserSnapshot) -> None:
        self._snapshot = snapshot

    def by_user(self) -> UserSnapshot:
        if self._snapshot is None:
            return UserSnapshot(key=UserKey("mail@mail.com"), todolist=())
        return self._snapshot


class CreateTodolist:
    def __init__(self, user_repository: UserRepositoryForTest, todolist_uuid_generator: TodolistUuidGeneratorForTest):
        self._todolist_uuid_generator = todolist_uuid_generator
        self._user_repository = user_repository

    def execute(self, user_key: UserKey, todolist_name: TodolistName) -> None:
        user_snapshot = self._user_repository.by_user()
        user_snapshot = replace(user_snapshot, todolist=(*user_snapshot.todolist, TodolistSnapshot(
            key=self._todolist_uuid_generator.generate_todolist_key(), name=todolist_name)))

        self._user_repository.save(user_snapshot)


class TestToto:
    def test_create_todolist(self, user_repository: UserRepositoryForTest,
                             todolist_uuid_generator: TodolistUuidGeneratorForTest,
                             sut: CreateTodolist):
        # GIVEN
        todolist_uuid: UUID = uuid4()
        todolist_uuid_generator.feed(next_uuid=todolist_uuid)

        # WHEN
        sut.execute(user_key=UserKey("mail@mail.com"), todolist_name=TodolistName("my todolist"))

        # THEN
        assert user_repository.by_user() == UserSnapshot(key=UserKey("mail@mail.com"),
                                                         todolist=(TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                    name=TodolistName("my todolist")),))

    def test_create_second_todolist(self, user_repository: UserRepositoryForTest,
                                    todolist_uuid_generator: TodolistUuidGeneratorForTest,
                                    sut: CreateTodolist):
        # GIVEN
        todolist_uuid = uuid4()
        todolist_uuid_generator.feed(next_uuid=todolist_uuid)
        first_todolist = TodolistSnapshot(key=TodolistKey(uuid4()), name=TodolistName("my first todolist"))
        user_repository.save(UserSnapshot(key=UserKey("mail@mail.com"), todolist=(first_todolist,)))

        # WHEN
        sut.execute(user_key=UserKey("mail@mail.com"), todolist_name=TodolistName("my second todolist"))

        # THEN
        assert user_repository.by_user() == UserSnapshot(key=UserKey("mail@mail.com"),
                                                         todolist=(first_todolist,
                                                                   TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                    name=TodolistName(
                                                                                        "my second todolist"))))

    @pytest.fixture
    def user_repository(self) -> UserRepositoryForTest:
        return UserRepositoryForTest()

    @pytest.fixture
    def todolist_uuid_generator(self) -> TodolistUuidGeneratorForTest:
        return TodolistUuidGeneratorForTest()

    @pytest.fixture
    def sut(self, user_repository: UserRepositoryForTest,
            todolist_uuid_generator: TodolistUuidGeneratorForTest) -> CreateTodolist:
        return CreateTodolist(user_repository=user_repository, todolist_uuid_generator=todolist_uuid_generator)
