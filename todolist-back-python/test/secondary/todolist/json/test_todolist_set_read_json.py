from dataclasses import replace
from pathlib import Path

import pytest
from faker import Faker

from dependencies import Dependencies
from primary.controller.read.todolist import Task, TodolistSetReadPort
from secondary.todolist.todolist_set_json import TodolistSetJson
from secondary.todolist.todolist_set_read_json import TodolistSetReadJson
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())

@pytest.fixture
def json_path(tmp_path: Path) -> Path:
    return tmp_path / "todolist.json"

@pytest.fixture
def dependencies(json_path: Path) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: json_path)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadJson.factory)
    return dependencies

@pytest.fixture
def sut(json_path: Path, dependencies: Dependencies) -> TodolistSetReadJson:
    return dependencies.get_adapter(TodolistSetReadPort)


def test_read_task_by(sut: TodolistSetReadJson, json_path: Path, fake: TodolistFaker):
    expected_task = fake.a_task()
    todolist = fake.a_todolist()
    TodolistSetJson(json_path).save_snapshot(replace(todolist, tasks=[fake.a_task(), expected_task, fake.a_task()]))

    assert sut.task_by(todolist_name=todolist.name, task_key=expected_task.key) == Task(id=expected_task.key, name=expected_task.name)


def test_read_all_by_name(sut: TodolistSetReadJson, json_path: Path, fake: TodolistFaker):
    todolist_1 = fake.a_todolist()
    todolist_2 = fake.a_todolist()
    todolist_3 = fake.a_todolist()
    TodolistSetJson(json_path).save_snapshot(todolist_1)
    TodolistSetJson(json_path).save_snapshot(todolist_2)
    TodolistSetJson(json_path).save_snapshot(todolist_3)

    assert sut.all_by_name() == [todolist_1.name, todolist_2.name, todolist_3.name]