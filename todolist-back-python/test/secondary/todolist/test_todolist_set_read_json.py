from dataclasses import replace
from pathlib import Path

import pytest
from faker import Faker

from primary.controller.read.todolist import Task
from secondary.todolist.todolist_set_json import TodolistSetJson
from secondary.todolist.todolist_set_read_json import TodolistSetReadJson
from test.hexagon.todolist.fixture import TodolistFaker


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_read_task_by(tmp_path: Path, fake: TodolistFaker):
    json_path = tmp_path / "todolist.json"
    expected_task = fake.a_task()
    todolist = fake.a_todolist()
    TodolistSetJson(json_path).save_snapshot(replace(todolist, tasks=[fake.a_task(), expected_task, fake.a_task()]))

    sut = TodolistSetReadJson(json_path)

    assert sut.task_by(todolist_name=todolist.name, task_key=expected_task.key.value) == Task(id=expected_task.key.value, name=expected_task.name)


def test_read_all_by_name(tmp_path: Path, fake: TodolistFaker):
    json_path = tmp_path / "todolist.json"
    todolist_1 = fake.a_todolist()
    todolist_2 = fake.a_todolist()
    todolist_3 = fake.a_todolist()
    TodolistSetJson(json_path).save_snapshot(todolist_1)
    TodolistSetJson(json_path).save_snapshot(todolist_2)
    TodolistSetJson(json_path).save_snapshot(todolist_3)

    sut = TodolistSetReadJson(json_path)

    assert sut.all_by_name() == [todolist_1.name, todolist_2.name, todolist_3.name]