import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mock.mock import MagicMock  # type: ignore

from src.hexagon.shared.type import TodolistKey
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.rest import start_app
from src.primary.todolist.read.port import AllTaskPort, AllTasksPresentation, TaskPresentation
from test.fixture import TodolistFaker, TaskBuilder
from test.primary.query_dependencies_not_implemented import QueryDependenciesNotImplemented
from test.primary.use_cases_dependencies_not_implemented import UseCaseDependenciesNotImplemented


class UseCasesForTest(UseCaseDependenciesNotImplemented):
    def __init__(self, use_case: MagicMock):
        self.use_case = use_case

    def open_task(self) -> OpenTaskUseCase:
        return self.use_case


class QueryDependenciesForTest(QueryDependenciesNotImplemented):
    def __init__(self, all_tasks: AllTaskPort):
        self._all_tasks = all_tasks

    def all_tasks(self) -> AllTaskPort:
        return self._all_tasks


class AllTaskForTest(AllTaskPort):
    def __init__(self) -> None:
        self._tasks_by_todolist : dict[TodolistKey, list[TaskBuilder]] = {}

    def all_tasks(self, todolist_key: TodolistKey) -> AllTasksPresentation:
        all_tasks_presentation = AllTasksPresentation(tasks=[self._to_presentation(task) for task in self._tasks_by_todolist[todolist_key]])
        return all_tasks_presentation

    def feed(self, todolist_key: TodolistKey, tasks: list[TaskBuilder]):
        self._tasks_by_todolist[todolist_key] = tasks

    @staticmethod
    def _to_presentation(task: TaskBuilder) -> TaskPresentation:
        return TaskPresentation(key=task.to_key(), name=task.to_name(), open=task.to_open(), execution_date=task.to_execution_date().default_value(None))


@pytest.fixture
def all_tasks() -> AllTaskForTest:
    return AllTaskForTest()

@pytest.fixture
def app(all_tasks: AllTaskForTest) -> FastAPI:
    return start_app(use_cases=UseCaseDependenciesNotImplemented(), queries=QueryDependenciesForTest(
        all_tasks=all_tasks))


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_list_all_tasks_when_no_task(client: TestClient, all_tasks: AllTaskForTest, app: FastAPI, fake: TodolistFaker):
    todolist = fake.a_todolist()
    all_tasks.feed(todolist_key=todolist.to_key(), tasks=[])
    response = client.get(f"/todolist/{todolist.to_key()}/task")

    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_list_all_tasks_when_task(client: TestClient, all_tasks: AllTaskForTest, app: FastAPI, fake: TodolistFaker):
    todolist = fake.a_todolist()
    task_one = fake.a_task()
    task_two = fake.a_task().having(execution_date=fake.a_date())
    all_tasks.feed(todolist_key=todolist.to_key(), tasks=[task_one, task_two])
    response = client.get(f"/todolist/{todolist.to_key()}/task")


    assert response.status_code == 200
    assert response.json() == {"tasks": [
        {"key": str(task_one.to_key()), "name": str(task_one.to_name()), "open": task_one.to_open(), "execution_date": None},
        {"key": str(task_two.to_key()), "name": task_two.to_name(), "open": task_two.to_open(), "execution_date": str(task_two.to_execution_date().value)},
    ]}
