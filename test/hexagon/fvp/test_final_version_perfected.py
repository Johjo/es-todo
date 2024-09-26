from uuid import uuid4, UUID

import pytest

from hexagon.fvp.domain_model import Task, NothingToDo, DoTheTask, ChooseTheTask, FinalVersionPerfected


def a_task_id(index: int = None):
    if index:
        return UUID(int=index, version=4)
    return uuid4()


@pytest.fixture
def sut():
    return FinalVersionPerfected()


def test_propose_nothing_when_empty(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_when_one_task_propose_the_only_task_open_when_one(sut):
    task = Task(id=uuid4(), name="buy milk")

    actual = sut.which_task([task])
    assert actual == DoTheTask(id=task.id, name=task.name)


def test_when_two_tasks_propose_to_choose_both(sut):
    open_task = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]

    actual = sut.which_task(open_task)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")


@pytest.mark.parametrize("chosen_task,ignored_task,expected", [
    (1, 2, DoTheTask(id=a_task_id(1), name="buy milk")),
    (2, 1, DoTheTask(id=a_task_id(2), name="buy water")),

])
def test_when_two_tasks_propose_to_do_chosen_task(sut, chosen_task, ignored_task, expected):
    sut.choose_and_ignore_task(id_chosen=a_task_id(chosen_task), id_ignored=a_task_id(ignored_task))

    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]
    actual = sut.which_task(open_tasks)
    assert actual == expected


def test_when_two_tasks_reopen_deffered_task_when_previous_task_is_done(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")


def test_when_two_propose_first_task_when_last_is_closed(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")


def test_when_three_evaluate_from_previous_chosen_task_when_close_one(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs")]

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(2))
    sut.choose_and_ignore_task(a_task_id(3), a_task_id(1))

    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")


def test_when_four_propose_tasks_in_good_order_after_close_one(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs"), Task(id=a_task_id(4), name="buy bread")]

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(1))
    sut.choose_and_ignore_task(a_task_id(3), a_task_id(2))
    sut.choose_and_ignore_task(a_task_id(3), a_task_id(4))
    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(2), name_1="buy water", id_2=a_task_id(4), name_2="buy bread")


### -----
def test_acceptance_with_no_tasks(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_acceptance_with_one_tasks(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk")]
    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")


def test_acceptance_with_two_tasks_01(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_two_tasks_02(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_01(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(2), name_1="buy water", id_2=a_task_id(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_02(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(1), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_id(3), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_03(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(2), name_1="buy water", id_2=a_task_id(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_id(3), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_four_tasks_01(sut):
    open_tasks = [Task(id=a_task_id(1), name="buy milk"), Task(id=a_task_id(2), name="buy water"),
                  Task(id=a_task_id(3), name="buy eggs"), Task(id=a_task_id(4), name="buy bread")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(2), name_1="buy water", id_2=a_task_id(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_id(3), a_task_id(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(3), name_1="buy eggs", id_2=a_task_id(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_id(3), a_task_id(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(3), name="buy eggs")  # here

    open_tasks.remove(Task(id=a_task_id(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(2), name_1="buy water", id_2=a_task_id(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_id(2), a_task_id(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(2), name="buy water")

    open_tasks.remove(Task(id=a_task_id(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_id(1), name_1="buy milk", id_2=a_task_id(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_id(4), a_task_id(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(4), name="buy bread")

    open_tasks.remove(Task(id=a_task_id(4), name="buy bread"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_id(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_id(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()

### -----
