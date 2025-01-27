from dataclasses import replace

import pytest
from faker import Faker

from src.hexagon.fvp.aggregate import Task, NothingToDo, DoTheTask, ChooseTheTask, FvpSnapshot
from src.hexagon.fvp.read.which_task import TodolistPort, WhichTaskQuery, WhichTaskFilter
from src.hexagon.shared.type import TodolistName
from test.fixture import a_task_key
from test.hexagon.fvp.write.fixture import FvpSessionSetForTest


class TodolistForTest(TodolistPort):
    def __init__(self) -> None:
        self._tasksByFilter: dict[WhichTaskFilter | None, list[Task]] = {}

    def all_open_tasks(self, task_filter: WhichTaskFilter | None) -> list[Task]:
        assert task_filter in self._tasksByFilter, "tasks must be fed before being read"
        return self._tasksByFilter[task_filter]

    def feed(self, task_filter: WhichTaskFilter, *tasks: Task):
        self._tasksByFilter[task_filter] = [task for task in tasks]


@pytest.fixture
def sut(fvp_session_set: FvpSessionSetForTest, todolist_name: TodolistForTest):
    return WhichTaskQuery(todolist_name, fvp_session_set)


@pytest.fixture
def todolist_name():
    return TodolistForTest()


@pytest.fixture
def fvp_session_set():
    return FvpSessionSetForTest()


class FvpFaker:
    def __init__(self, fake: Faker):
        self._fake: Faker = fake

    def a_task(self, key: None | int = None) -> Task:
        if key is None:
            key = self._fake.random_int()
        return Task(key=a_task_key(key))

    def a_which_task_filter(self) -> WhichTaskFilter:
        return WhichTaskFilter(todolist_name=TodolistName(self._fake.word()), reference_date=self._fake.date_object(),
                          include_context=(self._fake.word(),),
                          exclude_context=(self._fake.word(),))



@pytest.fixture
def fake() -> FvpFaker:
    return FvpFaker(Faker())


def test_which_task_without_tasks(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    task_filter = fake.a_which_task_filter()
    todolist_name.feed(task_filter)
    assert sut.which_task(task_filter) == NothingToDo()


def test_which_task_with_one_task(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    # GIVEN
    expected_task = replace(fake.a_task(1))
    task_filter = fake.a_which_task_filter()
    todolist_name.feed(task_filter, expected_task)

    # WHEN

    # THEN
    assert sut.which_task(task_filter) == DoTheTask(key=expected_task.key)


def test_which_task_with_two_tasks(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    primary_task = replace(fake.a_task(1))
    secondary_task = replace(fake.a_task(2))
    task_filter = fake.a_which_task_filter()
    todolist_name.feed(task_filter, primary_task, secondary_task)

    assert sut.which_task(task_filter) == ChooseTheTask(main_task_key=primary_task.key, secondary_task_key=secondary_task.key)


def test_load_existing_session(sut: WhichTaskQuery, todolist_name: TodolistForTest, fvp_session_set: FvpSessionSetForTest,
                               fake: FvpFaker):
    chosen_task = replace(fake.a_task(1))
    ignored_task = replace(fake.a_task(2))
    task_filter = fake.a_which_task_filter()

    fvp_session_set.feed(FvpSnapshot.from_primitive_dict({ignored_task.key: chosen_task.key}))
    todolist_name.feed(task_filter, chosen_task, ignored_task)

    assert sut.which_task(task_filter) == DoTheTask(key=chosen_task.key)
