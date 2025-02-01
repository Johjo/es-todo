from uuid import UUID, uuid4

import pytest

from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist
from src.hexagon.user.port import TodolistUuidGeneratorPort, UserRepositoryPort, UserSnapshot, TodolistSnapshot


class TodolistUuidGeneratorForTest(TodolistUuidGeneratorPort):
    def __init__(self) -> None:
        self._next_uuid: UUID | None = None

    def feed(self, next_uuid: UUID) -> None:
        self._next_uuid = next_uuid

    def generate_todolist_key(self) -> TodolistKey:
        if self._next_uuid is None:
            raise Exception("feed next_uuid before generating todolist key")
        return TodolistKey(self._next_uuid)


class UserRepositoryForTest(UserRepositoryPort):
    def __init__(self) -> None:
        self._snapshot: dict[UserKey, UserSnapshot] = {}

    def save(self, user: UserSnapshot) -> None:
        self._snapshot[user.key] = user

    def by_user(self, key: UserKey) -> UserSnapshot | None:
        return self._snapshot.get(key, None)


class TestCreateTodolist:
    def test_single_user_can_create_his_first_todolist(self, user_repository: UserRepositoryForTest,
                                                       todolist_uuid_generator: TodolistUuidGeneratorForTest,
                                                       sut: CreateTodolist):
        # GIVEN
        todolist_uuid: UUID = uuid4()
        todolist_uuid_generator.feed(next_uuid=todolist_uuid)
        user_key = self.any_user_key()

        # WHEN
        sut.execute(user_key=UserKey(user_key), todolist_name=TodolistName("my todolist"))

        # THEN
        assert user_repository.by_user(key=UserKey(user_key)) == UserSnapshot(key=UserKey(user_key),
                                                                              todolist=(
                                                                              TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                               name=TodolistName("my todolist")),))

    def test_single_user_can_create_many_todolist(self, user_repository: UserRepositoryForTest,
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
        assert user_repository.by_user(key=UserKey("mail@mail.com")) == UserSnapshot(key=UserKey("mail@mail.com"),
                                                                                     todolist=(first_todolist,
                                                                                               TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                                name=TodolistName(
                                                                                        "my second todolist"))))

    def test_many_users_can_create_todolist(self, user_repository: UserRepositoryForTest,
                                            todolist_uuid_generator: TodolistUuidGeneratorForTest,
                                            sut: CreateTodolist):
        # GIVEN
        todolist_uuid: UUID = uuid4()
        todolist_uuid_generator.feed(next_uuid=todolist_uuid)
        user_key_1 = self.any_user_key()
        user_key_2 = self.any_user_key()

        # WHEN
        sut.execute(user_key=UserKey(user_key_1), todolist_name=TodolistName("my todolist for user 1"))
        sut.execute(user_key=UserKey(user_key_2), todolist_name=TodolistName("my todolist for user 2"))

        # THEN
        assert user_repository.by_user(key=UserKey(user_key_1)) == UserSnapshot(key=UserKey(user_key_1),
                                                                                todolist=(
                                                                                TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                 name=TodolistName("my todolist for user 1")),))
        assert user_repository.by_user(key=UserKey(user_key_2)) == UserSnapshot(key=UserKey(user_key_2),
                                                                                todolist=(
                                                                                TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                 name=TodolistName("my todolist for user 2")),))

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

    @staticmethod
    def any_user_key():
        return f'mail{uuid4()}@mail.com'

