from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mock.mock import MagicMock  # type: ignore

from src.hexagon.user.create_todolist import CreateTodolist
from src.primary.rest import start_app
from test.primary.query_dependencies_not_implemented import QueryDependenciesNotImplemented
from test.primary.use_cases_dependencies_not_implemented import UseCaseDependenciesNotImplemented


class UseCaseDependenciesForTest(UseCaseDependenciesNotImplemented):
    def __init__(self, use_case: MagicMock):
        self.use_case = use_case

    def create_todolist(self) -> CreateTodolist:
        return self.use_case


@pytest.fixture
def use_case() -> MagicMock:
    return MagicMock()  # type: ignore


@pytest.fixture
def app(use_case: MagicMock) -> FastAPI:
    return start_app(use_cases=UseCaseDependenciesForTest(use_case), queries=QueryDependenciesNotImplemented())


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_create_todolist(client: TestClient, use_case: MagicMock, app: FastAPI):
    todolist_name = any_todolist_name()
    user = any_user()
    todolist_key = uuid4()
    response = client.post(f"/{user}/todolist/{todolist_key}", json={"name": todolist_name})

    assert response.status_code == 200
    assert response.json() is None
    use_case.execute.assert_called_with(user_key=user, todolist_key=todolist_key, todolist_name=todolist_name)


def any_user():
    return f'mail{uuid4()}@mail.com'


def any_todolist_name():
    return "todolist_name" + str(uuid4())
