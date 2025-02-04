from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.primary.web.pages import bottle_config
from test.primary.web.fixture import CleanResponse, header_with_good_authentication


def test_create_todolist(dependencies: Dependencies, app: TestApp) -> None:
    bottle_config.dependencies = dependencies
    response = app.post('/todo', params={'name': "my_created_todolist"}, headers=header_with_good_authentication())

    assert CleanResponse(response).location() == "/todo/my_created_todolist"
    assert response.status_code == 302

from uuid import UUID, uuid4

import pytest

from src.dependencies import Dependencies
from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist
from src.hexagon.user.port import TodolistUuidGeneratorPort, UserRepositoryPort, UserSnapshot, TodolistSnapshot
from src.primary.controller.user import UserController
from src.secondary.user.user_repository_in_memory import UserRepositoryInMemory


class TodolistUuidGeneratorForTest(TodolistUuidGeneratorPort):
    def __init__(self) -> None:
        self._next_uuid: UUID | None = None

    def feed(self, next_uuid: UUID) -> None:
        self._next_uuid = next_uuid

    def generate_todolist_key(self) -> TodolistKey:
        if self._next_uuid is None:
            raise Exception("feed next_uuid before generating todolist key")
        return TodolistKey(self._next_uuid)


class TestCreateTodolist:
    def test_single_user_can_create_his_first_todolist(self, dependencies: Dependencies,
                                                       user_repository: UserRepositoryInMemory,
                                                       todolist_uuid_generator: TodolistUuidGeneratorForTest):
        # GIVEN
        todolist_uuid: UUID = uuid4()
        todolist_uuid_generator.feed(next_uuid=todolist_uuid)
        user_key = self.any_user_key()

        # WHEN
        sut = UserController(dependencies)
        sut.create_todolist(user_key=user_key, todolist_name="my todolist")

        # THEN
        assert user_repository.by_user(key=UserKey(user_key)) == UserSnapshot(key=UserKey(user_key),
                                                                              todolist=(
                                                                              TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                               name=TodolistName("my todolist")),))



    @pytest.fixture
    def dependencies(self, user_repository: UserRepositoryInMemory, todolist_uuid_generator: TodolistUuidGeneratorForTest) -> Dependencies:
        dependencies = Dependencies.create_empty()
        dependencies = dependencies.feed_use_case(CreateTodolist, CreateTodolist.factory)
        dependencies = dependencies.feed_adapter(UserRepositoryPort, lambda _: user_repository)
        dependencies = dependencies.feed_adapter(TodolistUuidGeneratorPort, lambda _: todolist_uuid_generator)
        return dependencies

    @pytest.fixture
    def user_repository(self) -> UserRepositoryInMemory:
        return UserRepositoryInMemory()

    @pytest.fixture
    def todolist_uuid_generator(self) -> TodolistUuidGeneratorForTest:
        return TodolistUuidGeneratorForTest()

    @staticmethod
    def any_user_key():
        return f'mail{uuid4()}@mail.com'

