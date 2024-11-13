from pathlib import Path

import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Some, Nothing

from infra.json_file import JsonFile


@pytest.fixture
def json_path(tmp_path) -> Path:
    return tmp_path / "test_todolist.json"


def test_insert_many_values(json_path: Path):
    sut = JsonFile(json_path)
    sut.insert("todolist 1", {"name": "todolist 1", "key": "value"})
    sut.insert("todolist 2", {"name": "todolist 2", "key": "value"})

    verify(json_path.read_text(), reporter=PythonNativeReporter())


def test_read_value(json_path: Path):
    sut = JsonFile(json_path)
    sut.insert("todolist 1", {"name": "todolist 1", "key": "value"})
    sut.insert("todolist 2", {"name": "todolist 2", "key": "value"})

    assert sut.read("todolist 2") == Some({"name": "todolist 2", "key": "value"})

def test_return_nothing_when_read_unknown_value(json_path: Path):
    sut = JsonFile(json_path)

    assert sut.read("unknown value") == Nothing



def test_read_all_keys(json_path: Path):
    sut = JsonFile(json_path)

    sut.insert("todolist 1", {"name": "todolist 1", "key": "value"})
    sut.insert("todolist 2", {"name": "todolist 2", "key": "value"})

    assert sut.all_keys() == ["todolist 1", "todolist 2"]
