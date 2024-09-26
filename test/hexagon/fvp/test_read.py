from collections import OrderedDict
from uuid import UUID, uuid4

import pytest

from test.hexagon.fvp.test_double import SimpleFvpSessionRepository
from hexagon.fvp.domain_model import NothingToDo, DoTheTask, Task, ChooseTheTask, FvpSnapshot
from hexagon.fvp.read.which_task import TaskReader, WhichTaskQuery


class SimpleTaskReader(TaskReader):
    def all(self) -> list[Task]:
        return self._tasks

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def feed(self, task) -> None:
        self._tasks.append(task)


def a_task_id(index: int | None = None):
    if index:
        return UUID(int=index, version=4)
    return uuid4()


@pytest.fixture
def sut(set_of_fvp_sessions: SimpleFvpSessionRepository, set_of_open_tasks: SimpleTaskReader):
    return WhichTaskQuery(set_of_open_tasks, set_of_fvp_sessions)


@pytest.fixture
def set_of_open_tasks():
    return SimpleTaskReader()


@pytest.fixture
def set_of_fvp_sessions():
    return SimpleFvpSessionRepository()


def test_which_task_without_tasks(sut):
    assert sut.which_task() == NothingToDo()


def test_which_task_with_one_task(sut, set_of_open_tasks):
    set_of_open_tasks.feed(Task(id=a_task_id(1), name="buy milk"))
    assert sut.which_task() == DoTheTask(id=a_task_id(1), name="buy milk")


def test_which_task_with_two_tasks(sut, set_of_open_tasks):
    set_of_open_tasks.feed(Task(id=a_task_id(1), name="buy milk"))
    set_of_open_tasks.feed(Task(id=a_task_id(2), name="buy water"))
    assert sut.which_task() == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2),
                                             name_2="buy water")


def test_load_existing_session(sut, set_of_open_tasks, set_of_fvp_sessions):
    set_of_fvp_sessions.feed(FvpSnapshot(OrderedDict[uuid4, int]({a_task_id(1): 1, a_task_id(2): 0})))
    set_of_open_tasks.feed(Task(id=a_task_id(1), name="buy milk"))
    set_of_open_tasks.feed(Task(id=a_task_id(2), name="buy water"))

    assert sut.which_task() == DoTheTask(id=a_task_id(1), name="buy milk")
