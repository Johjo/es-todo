from collections import OrderedDict

import pytest

from test.fixture import a_task_key
from hexagon.fvp.aggregate import Task, NothingToDo, DoTheTask, ChooseTheTask, FinalVersionPerfectedSession, \
    FvpSnapshot


@pytest.fixture
def sut():
    return FinalVersionPerfectedSession.create()


def test_propose_nothing_when_empty(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_when_one_task_propose_the_only_task_open_when_one(sut):
    task = Task(id=1, name="buy milk")

    actual = sut.which_task([task])
    assert actual == DoTheTask(id=task.id, name=task.name)


def test_when_two_tasks_propose_to_choose_both(sut):
    open_task = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]

    actual = sut.which_task(open_task)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")


@pytest.mark.parametrize("chosen_task,ignored_task,expected", [
    (1, 2, DoTheTask(id=a_task_key(1), name="buy milk")),
    (2, 1, DoTheTask(id=a_task_key(2), name="buy water")),

])
def test_when_two_tasks_propose_to_do_chosen_task(sut, chosen_task, ignored_task, expected):
    sut.choose_and_ignore_task(id_chosen=a_task_key(chosen_task), id_ignored=a_task_key(ignored_task))

    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]
    actual = sut.which_task(open_tasks)
    assert actual == expected


def test_when_two_tasks_reopen_deffered_task_when_previous_task_is_done(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")


def test_when_two_propose_first_task_when_last_is_closed(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")


def test_when_three_evaluate_from_previous_chosen_task_when_close_one(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs")]

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")


def test_when_four_propose_tasks_in_good_order_after_close_one(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs"), Task(id=a_task_key(4), name="buy bread")]

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))
    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))
    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(2), name_1="buy water", id_2=a_task_key(4), name_2="buy bread")


### -----
def test_acceptance_with_no_tasks(sut):
    actual = sut.which_task([])
    assert actual == NothingToDo()


def test_acceptance_with_one_tasks(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk")]
    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")


def test_acceptance_with_two_tasks_01(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_two_tasks_02(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_01(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(2), name_1="buy water", id_2=a_task_key(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_02(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_03(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(2), name_1="buy water", id_2=a_task_key(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(3), name="buy eggs")

    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


def test_acceptance_with_four_tasks_01(sut):
    open_tasks = [Task(id=a_task_key(1), name="buy milk"), Task(id=a_task_key(2), name="buy water"),
                  Task(id=a_task_key(3), name="buy eggs"), Task(id=a_task_key(4), name="buy bread")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(2), name_2="buy water")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(2), name_1="buy water", id_2=a_task_key(3), name_2="buy eggs")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(3), name_1="buy eggs", id_2=a_task_key(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(3), name="buy eggs")  # here

    open_tasks.remove(Task(id=a_task_key(3), name="buy eggs"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(2), name_1="buy water", id_2=a_task_key(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_key(2), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(2), name="buy water")

    open_tasks.remove(Task(id=a_task_key(2), name="buy water"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="buy milk", id_2=a_task_key(4), name_2="buy bread")

    sut.choose_and_ignore_task(a_task_key(4), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(4), name="buy bread")

    open_tasks.remove(Task(id=a_task_key(4), name="buy bread"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(1), name="buy milk")

    open_tasks.remove(Task(id=a_task_key(1), name="buy milk"))

    actual = sut.which_task(open_tasks)
    assert actual == NothingToDo()


# - [ ] Email  #testfvp
# - [ ] In-Tray #testfvp
# - [ ] (3) Voicemail #testfvp
# - [ ] Project X Report #testfvp
# - [ ] (1) Tidy Desk #testfvp
# - [ ] Call Dissatisfied Customer #testfvp
# - [ ] (4) Make Dental Appointment #testfvp
# - [ ] File Invoices #testfvp
# - [ ] Discuss Project Y with Bob #testfvp
# - [ ] (2)Back Up   #testfvp


def test_acceptance_full(sut):
    open_tasks = [Task(id=a_task_key(1), name="email"), Task(id=a_task_key(2), name="In-Tray"),
                  Task(id=a_task_key(3), name="voicemail"), Task(id=a_task_key(4), name="Project X Report"),
                  Task(id=a_task_key(5), name="Tidy Desk"), Task(id=a_task_key(6), name="Call Dissatisfied Customer"),
                  Task(id=a_task_key(7), name="Make Dental Appointment"), Task(id=a_task_key(8), name="File Invoices"),
                  Task(id=a_task_key(9), name="Discuss Project Y with Bob"), Task(id=a_task_key(10), name="Back Up")]

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="email", id_2=a_task_key(2), name_2="In-Tray")

    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(1), name_1="email", id_2=a_task_key(3), name_2="voicemail")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(1))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(3), name_1="voicemail", id_2=a_task_key(4), name_2="Project X Report")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(4))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(3), name_1="voicemail", id_2=a_task_key(5), name_2="Tidy Desk")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(5), name_1="Tidy Desk", id_2=a_task_key(6), name_2="Call Dissatisfied Customer")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(6))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(5), name_1="Tidy Desk", id_2=a_task_key(7), name_2="Make Dental Appointment")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(7))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(5), name_1="Tidy Desk", id_2=a_task_key(8), name_2="File Invoices")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(8))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(5), name_1="Tidy Desk", id_2=a_task_key(9), name_2="Discuss Project Y with Bob")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(9))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(5), name_1="Tidy Desk", id_2=a_task_key(10), name_2="Back Up")

    sut.choose_and_ignore_task(a_task_key(5), a_task_key(10))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(5), name="Tidy Desk")

    open_tasks.remove(Task(id=a_task_key(5), name="Tidy Desk"))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(3), name_1="voicemail", id_2=a_task_key(6), name_2="Call Dissatisfied Customer")

    sut.choose_and_ignore_task(a_task_key(3), a_task_key(6))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(3), name_1="voicemail", id_2=a_task_key(7), name_2="Make Dental Appointment")

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(3))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(7), name_1="Make Dental Appointment", id_2=a_task_key(8), name_2="File Invoices")

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(8))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(7), name_1="Make Dental Appointment", id_2=a_task_key(9), name_2="Discuss Project Y with Bob")

    sut.choose_and_ignore_task(a_task_key(7), a_task_key(9))

    actual = sut.which_task(open_tasks)
    assert actual == ChooseTheTask(id_1=a_task_key(7), name_1="Make Dental Appointment", id_2=a_task_key(10), name_2="Back Up")

    sut.choose_and_ignore_task(a_task_key(10), a_task_key(7))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(id=a_task_key(10), name="Back Up")

    open_tasks.remove(Task(id=a_task_key(10), name="Back Up"))

    actual = sut.which_task(open_tasks)
    assert actual == DoTheTask(a_task_key(7), name="Make Dental Appointment")





def test_empty_snapshot(sut):
    snapshot = sut.to_snapshot()
    d = OrderedDict()
    assert snapshot == FvpSnapshot(OrderedDict())

def test_write_priorities_to_snapshot(sut):
    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    snapshot = sut.to_snapshot()
    assert snapshot == FvpSnapshot(OrderedDict({a_task_key(2): a_task_key(1)}))

def test_read_priorities_from_snapshot(sut):
    snapshot = FvpSnapshot(OrderedDict({a_task_key(1): 1, a_task_key(2): 0}))
    sut = FinalVersionPerfectedSession.from_snapshot(snapshot)
    assert sut.to_snapshot() == FvpSnapshot(OrderedDict({a_task_key(1): 1, a_task_key(2): 0}))

def test_reset_session(sut):
    sut.choose_and_ignore_task(a_task_key(1), a_task_key(2))
    sut.reset()
    assert sut.to_snapshot() == FvpSnapshot(OrderedDict())
