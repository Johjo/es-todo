from dataclasses import replace
from pathlib import Path

import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Some
from faker import Faker

from infra.json_file import JsonFile
from dependencies import Dependencies
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def json_path(tmp_path) -> Path:
    return tmp_path / "test_todolist.json"


@pytest.fixture
def sut(json_path: Path) -> TodolistSetJson:
    return TodolistSetJson(JsonFile(json_path))


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_save_two_todolist(fake: TodolistFaker, json_path: Path, sut: TodolistSetJson):
    sut.save_snapshot(replace(fake.a_todolist(), name="todolist_1", tasks=[replace(fake.a_task(1), name="buy milk"), replace(fake.a_task(2), name="buy water", is_open=False)]))
    sut.save_snapshot(replace(fake.a_todolist(), name="todolist_2", tasks=[replace(fake.a_task(1), name="buy eggs", is_open=False), replace(fake.a_task(5), name="buy bread")]))

    verify(json_path.read_text(), reporter=PythonNativeReporter())


def test_read_todolist(fake: TodolistFaker, json_path: Path, sut: TodolistSetJson) -> None:
    expected_todolist = replace(fake.a_todolist(), name="todolist_1", tasks=[replace(fake.a_task(1), name="buy milk", is_open=True), replace(fake.a_task(1), name="buy milk", is_open=False)])

    sut.save_snapshot(expected_todolist)

    assert sut.by(expected_todolist.name) == Some(expected_todolist)
