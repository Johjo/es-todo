import json
import os
from dataclasses import replace

import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Option, Some
from faker import Faker

from hexagon.todolist.aggregate import TodolistSetPort, TodolistSnapshot, TaskSnapshot, TaskKey
from test.hexagon.todolist.fixture import TodolistFaker


class TodolistSetJson(TodolistSetPort):
    def __init__(self, filename: str):
        self._filename = filename

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        d = {**(self._load_json()), todolist.name: self._to_todolist_dict(todolist)}

        with open(self._filename, "w") as f:
            f.write(json.dumps(d))

    def _to_todolist_dict(self, todolist: TodolistSnapshot):
        return {"name": todolist.name, "tasks": [self._to_task_dict(task) for task in todolist.tasks]}

    @staticmethod
    def _to_task_dict(task: TaskSnapshot):
        return {"key": task.key.value, "name": task.name, "is_open": task.is_open}

    def _load_json(self):
        try:
            f = open(self._filename, "r")
        except FileNotFoundError:
            d = {}
        else:
            with f:
                d = json.load(f)
        return d

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        d = self._load_json()
        d1 = {**d[todolist_name]}
        return Some(self._todolist_from_dict(d1))

    def _todolist_from_dict(self, d):
        return TodolistSnapshot(name=d["name"], tasks=[self._task_from_dict(task) for task in d["tasks"]])

    @staticmethod
    def _task_from_dict(d):
        return TaskSnapshot(key=TaskKey(d["key"]), name=d["name"], is_open=d["is_open"])


def ensure_directory_exist(path: str ) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def test_save_todolist():
    fake = TodolistFaker(Faker())
    ensure_directory_exist("data_test")
    filename = "data_test/test_todolist_set_01.json"
    ensure_file_does_not_exist(filename)
    todolist_set = TodolistSetJson(filename)
    todolist_set.save_snapshot(
        replace(fake.a_todolist(), name="my_todolist", tasks=[replace(fake.a_task(1), name="buy milk")]))

    with open(filename, "r") as f:
        verify(f.read(), reporter=PythonNativeReporter())


def ensure_file_does_not_exist(filename):
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_save_two_todolist(fake: TodolistFaker) -> None:
    filename = "data_test/test_todolist_set_02.json"

    ensure_file_does_not_exist(filename)

    todolist_set = TodolistSetJson(filename)
    todolist_set.save_snapshot(replace(fake.a_todolist(), name="todolist_1"))
    todolist_set.save_snapshot(replace(fake.a_todolist(), name="todolist_2"))

    with open(filename, "r") as f:
        verify(f.read(), reporter=PythonNativeReporter())


def test_read_todolist(fake: TodolistFaker) -> None:
    filename = "data_test/test_todolist_set_03.json"

    ensure_file_does_not_exist(filename)

    todolist_set = TodolistSetJson(filename)
    todolist = replace(fake.a_todolist(), name="todolist_1", tasks=[replace(fake.a_task(1), name="buy milk")])

    todolist_set.save_snapshot(todolist)

    assert todolist_set.by(todolist.name) == Some(todolist)
