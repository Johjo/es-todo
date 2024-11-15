from dataclasses import replace

import pytest
from faker import Faker

from dependencies import Dependencies
from hexagon.fvp.aggregate import DoTheTask, FvpSnapshot, FvpSessionSetPort
from hexagon.fvp.read.which_task import TodolistPort
from primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.hexagon.fvp.read.test_which_task import TodolistForTest, FvpFaker


@pytest.fixture
def todolist():
    return TodolistForTest()


@pytest.fixture
def fvp_session_set():
    return FvpSessionSetForTest()


@pytest.fixture
def fake() -> FvpFaker:
    return FvpFaker(Faker())


def test_which_task_when_two_and_one_chosen(dependencies: Dependencies, todolist: TodolistForTest,
                                            fvp_session_set: FvpSessionSetForTest,
                                            fake: FvpFaker):
    ignored_task = replace(fake.a_task(2), name="buy water")
    chosen_task = replace(fake.a_task(1), name="buy milk")
    task_filter = fake.a_which_task_filter()
    fvp_session_set.feed(FvpSnapshot.from_primitive_dict({ignored_task.id: chosen_task.id}))
    todolist.feed(task_filter, chosen_task, ignored_task)

    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: fvp_session_set)
    dependencies = dependencies.feed_adapter(TodolistPort, lambda _: todolist)

    actual = FinalVersionPerfectedReadController(dependencies).which_task(task_filter)

    assert actual == DoTheTask(id=chosen_task.id, name=chosen_task.name)
