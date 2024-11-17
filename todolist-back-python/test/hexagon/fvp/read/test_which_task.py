from dataclasses import replace

import pytest
from faker import Faker

from hexagon.fvp.aggregate import Task, NothingToDo, DoTheTask, ChooseTheTask, FvpSnapshot
from hexagon.fvp.read.which_task import TodolistPort, WhichTaskQuery, WhichTaskFilter
from hexagon.shared.type import TodolistName
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.fixture import a_task_key


class TodolistForTest(TodolistPort):
    def __init__(self) -> None:
        self._tasksByFilter: dict[WhichTaskFilter | None, list[Task]] = {}

    def all_open_tasks(self, task_filter: WhichTaskFilter | None) -> list[Task]:
        assert task_filter in self._tasksByFilter, "tasks must be fed before being read"
        return self._tasksByFilter[task_filter]

    def feed(self, task_filter: WhichTaskFilter, *tasks: Task):
        self._tasksByFilter[task_filter] = [task for task in tasks]


@pytest.fixture
def sut(fvp_session_set: FvpSessionSetForTest, todolist: TodolistForTest):
    return WhichTaskQuery(todolist, fvp_session_set)


@pytest.fixture
def todolist():
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
        return Task(id=a_task_key(key), name=self._fake.sentence())

    def a_which_task_filter(self) -> WhichTaskFilter:
        return WhichTaskFilter(todolist_name=TodolistName(self._fake.word()), reference_date=self._fake.date_object(),
                          include_context=(self._fake.word(),),
                          exclude_context=(self._fake.word(),))



@pytest.fixture
def fake() -> FvpFaker:
    return FvpFaker(Faker())


def test_which_task_without_tasks(sut: WhichTaskQuery, todolist: TodolistForTest, fake: FvpFaker):
    task_filter = fake.a_which_task_filter()
    todolist.feed(task_filter)
    assert sut.which_task(task_filter) == NothingToDo()


def test_which_task_with_one_task(sut: WhichTaskQuery, todolist: TodolistForTest, fake: FvpFaker):
    expected_task = replace(fake.a_task(1), name="buy milk")
    task_filter = fake.a_which_task_filter()
    todolist.feed(task_filter, expected_task)

    assert sut.which_task(task_filter) == DoTheTask(id=expected_task.id, name=expected_task.name)


def test_which_task_with_two_tasks(sut: WhichTaskQuery, todolist: TodolistForTest, fake: FvpFaker):
    primary_task = replace(fake.a_task(1), name="buy milk")
    secondary_task = replace(fake.a_task(2), name="buy water")
    task_filter = fake.a_which_task_filter()
    todolist.feed(task_filter, primary_task, secondary_task)

    assert sut.which_task(task_filter) == ChooseTheTask(id_1=primary_task.id, name_1=primary_task.name,
                                                        id_2=secondary_task.id, name_2=secondary_task.name)


def test_load_existing_session(sut: WhichTaskQuery, todolist: TodolistForTest, fvp_session_set: FvpSessionSetForTest,
                               fake: FvpFaker):
    chosen_task = replace(fake.a_task(1), name="buy milk")
    ignored_task = replace(fake.a_task(2), name="buy water")
    task_filter = fake.a_which_task_filter()

    fvp_session_set.feed(FvpSnapshot.from_primitive_dict({ignored_task.id: chosen_task.id}))
    todolist.feed(task_filter, chosen_task, ignored_task)

    assert sut.which_task(task_filter) == DoTheTask(id=chosen_task.id, name=chosen_task.name)
