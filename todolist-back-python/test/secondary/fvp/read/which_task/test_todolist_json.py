from dataclasses import replace
from pathlib import Path

import pytest
from faker import Faker

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from secondary.fvp.read.which_task.todolist_json import TodolistJson
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.fixture import TodolistFaker


@pytest.fixture
def json_path(tmp_path: Path) -> Path:
    return tmp_path / "todolist.json"


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


@pytest.fixture
def dependencies(json_path: Path) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistJson.factory)
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: json_path)
    return dependencies


@pytest.fixture
def sut(json_path: Path, dependencies: Dependencies) -> TodolistJson:
    return dependencies.get_adapter(TodolistPort)


def test_should_list_open_tasks(sut: TodolistJson, json_path: Path, fake: TodolistFaker):
    expected_tasks = [fake.a_task_old(), fake.a_task_old()]
    expected_todolist = replace(fake.a_todolist_old(), tasks=[*expected_tasks, replace(fake.a_task_old(), is_open=False)])
    another_todolist = replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()])

    TodolistSetJson(json_path).save_snapshot(expected_todolist)
    TodolistSetJson(json_path).save_snapshot(another_todolist)

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name)) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]


def test_should_no_task_when_todolist_does_not_exist(json_path: Path, fake: TodolistFaker):
    unknown_todolist = fake.a_todolist_old()
    another_todolist = replace(fake.a_todolist_old(), tasks=[fake.a_task_old(), fake.a_task_old()])

    TodolistSetJson(json_path).save_snapshot(another_todolist)

    sut = TodolistJson(json_path)

    assert sut.all_open_tasks(TaskFilter(todolist_name=unknown_todolist.name)) == []


def test_should_no_task_when_todolist_file_does_not_exist(json_path: Path, fake: TodolistFaker):
    unknown_todolist = fake.a_todolist_old()

    sut = TodolistJson(json_path)

    assert sut.all_open_tasks(TaskFilter(todolist_name=unknown_todolist.name)) == []
