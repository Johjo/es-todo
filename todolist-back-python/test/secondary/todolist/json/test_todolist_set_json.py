from dataclasses import replace
from pathlib import Path

import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Some, Nothing
from faker import Faker

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.fixture import TodolistFaker


@pytest.fixture
def json_path(tmp_path) -> Path:
    return tmp_path / "test_todolist.json"


@pytest.fixture
def dependencies(json_path: Path) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: json_path)
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetJson.factory)
    return dependencies


@pytest.fixture
def sut(json_path: Path, dependencies: Dependencies) -> TodolistSetJson:
    return dependencies.get_adapter(TodolistSetPort)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_save_two_todolist(fake: TodolistFaker, json_path: Path, sut: TodolistSetJson):
    sut.save_snapshot(replace(fake.a_todolist_old(), name="todolist_1", tasks=[replace(fake.a_task_old(1), name="buy milk"),
                                                                               replace(fake.a_task_old(2), name="buy water",
                                                                                   is_open=False)]))
    sut.save_snapshot(replace(fake.a_todolist_old(), name="todolist_2",
                              tasks=[replace(fake.a_task_old(1), name="buy eggs", is_open=False),
                                     replace(fake.a_task_old(5), name="buy bread")]))

    verify(json_path.read_text(), reporter=PythonNativeReporter())


def test_read_todolist(fake: TodolistFaker, json_path: Path, sut: TodolistSetJson) -> None:
    expected_todolist = replace(fake.a_todolist_old(), name="todolist_1",
                                tasks=[replace(fake.a_task_old(1), name="buy milk", is_open=True),
                                       replace(fake.a_task_old(1), name="buy milk", is_open=False)])

    sut.save_snapshot(expected_todolist)

    assert sut.by(expected_todolist.name) == Some(expected_todolist)

def test_return_nothing_when_todolist_does_not_exist(fake: TodolistFaker, json_path: Path, sut: TodolistSetJson) -> None:
    unknown_todolist = fake.a_todolist_old()
    assert sut.by(unknown_todolist.name) == Nothing
