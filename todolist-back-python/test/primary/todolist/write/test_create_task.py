import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mock.mock import MagicMock  # type: ignore

from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.rest import start_app
from test.fixture import TodolistFaker
from test.primary.query_dependencies_not_implemented import QueryDependenciesNotImplemented
from test.primary.use_cases_dependencies_not_implemented import UseCaseDependenciesNotImplemented


class UseCasesForTest(UseCaseDependenciesNotImplemented):
    def __init__(self, use_case: MagicMock):
        self.use_case = use_case

    def open_task(self) -> OpenTaskUseCase:
        return self.use_case

    def create_todolist(self) -> TodolistCreate:
        return self.use_case


@pytest.fixture
def use_case() -> MagicMock:
    return MagicMock()  # type: ignore


@pytest.fixture
def app(use_case: MagicMock) -> FastAPI:
    return start_app(use_cases=UseCasesForTest(use_case), queries=QueryDependenciesNotImplemented())


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_create_task(client: TestClient, use_case: MagicMock, app: FastAPI, fake: TodolistFaker):
    todolist = fake.a_todolist()
    task = fake.a_task()
    response = client.post(f"/todolist/{todolist.to_key()}/task/{task.to_key()}", json={"name": task.to_name()})

    assert response.status_code == 200
    assert response.json() is None
    use_case.execute.assert_called_with(todolist_key=todolist.to_key(), task_key=task.to_key(), name=task.to_name())
