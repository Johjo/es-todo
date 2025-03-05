import pytest
from expression import Result, Ok
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mock.mock import MagicMock  # type: ignore

from src.hexagon.shared.type import TodolistKey, TaskKey
from src.hexagon.todolist.write.close_task import CloseTaskPrimaryPort
from src.primary.rest import start_app
from test.fixture import TodolistFaker
from test.primary.query_dependencies_not_implemented import QueryDependenciesNotImplemented
from test.primary.use_cases_dependencies_not_implemented import UseCaseDependenciesNotImplemented


class UseCasesForTest(UseCaseDependenciesNotImplemented):
    def __init__(self, use_case: CloseTaskPrimaryPort):
        self.use_case = use_case

    def close_task(self) -> CloseTaskPrimaryPort:
        return self.use_case


class CloseTaskForTest(CloseTaskPrimaryPort):
    def __init__(self):
        self._history = []

    def execute(self, todolist_key: TodolistKey, task_key: TaskKey) -> Result[None, str]:
        self._history.append({"todolist_key": todolist_key, "task_key": task_key})
        return Ok(None)

    def history(self) -> list:
        return self._history


@pytest.fixture
def use_case() -> CloseTaskForTest:
    return CloseTaskForTest()


@pytest.fixture
def app(use_case: MagicMock) -> FastAPI:
    return start_app(use_cases=UseCasesForTest(use_case), queries=QueryDependenciesNotImplemented())


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_when_nothing(use_case: CloseTaskForTest):
    assert use_case.history() == []


def test_close_task(client: TestClient, use_case: CloseTaskForTest, app: FastAPI, fake: TodolistFaker):
    todolist = fake.a_todolist()
    task = fake.a_task()

    response = client.put(f"/todolist/{todolist.to_key()}/task/{task.to_key()}/close", json={"name": task.to_name()})
    assert response.status_code == 200
    assert response.json() is None
    assert use_case.history() == [{"todolist_key": todolist.to_key(), "task_key": task.to_key()}]
