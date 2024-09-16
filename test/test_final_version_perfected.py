import pytest

from domain.todoapp import TodoApp
from domain.presentation import NothingToDo, DoTheTask, ChooseTheTask


def test_propose_nothing_when_empty():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_propose_the_only_task_open_when_one():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")


def test_propose_nothing_when_all_tasks_are_closed():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_propose_to_choose_when_two_open_tasks():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")


def test_reopen_deffered_task_when_previous_task_is_done():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.choose_and_ignore_task(todolist_id, 1, 2)
    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")


def test_evaluate_task_after_closed_one():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")
    app.choose_and_ignore_task(todolist_id, 1, 2)
    app.choose_and_ignore_task(todolist_id, 1, 3)
    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=3, name_2="buy eggs")


def test_evaluate_from_previous_chosen_task_when_close_one():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")

    app.choose_and_ignore_task(todolist_id, 1, 2)
    app.choose_and_ignore_task(todolist_id, 3, 1)
    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

def test_xxx():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")
    app.add_item(todolist_id, "buy bread")

    app.choose_and_ignore_task(todolist_id, 2, 1)
    app.choose_and_ignore_task(todolist_id, 3, 2)
    app.choose_and_ignore_task(todolist_id, 3, 4)
    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=4, name_2="buy bread")

### -----


def test_acceptance_with_no_tasks():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_one_tasks():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_two_tasks_01():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 1, 2)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_two_tasks_02():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 2, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_01():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 1, 2)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=3, name_2="buy eggs")

    app.choose_and_ignore_task(todolist_id, 1, 3)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=3, name_2="buy eggs")

    app.choose_and_ignore_task(todolist_id, 2, 3)
    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=3, name="buy eggs")

    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_02():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 1, 2)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=3, name_2="buy eggs")

    app.choose_and_ignore_task(todolist_id, 3, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=3, name="buy eggs")

    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_three_tasks_03():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 2, 1)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=3, name_2="buy eggs")

    app.choose_and_ignore_task(todolist_id, 3, 2)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=3, name="buy eggs")

    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()


def test_acceptance_with_four_tasks_01():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")
    app.add_item(todolist_id, "buy bread")

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")

    app.choose_and_ignore_task(todolist_id, 2, 1)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=3, name_2="buy eggs")

    app.choose_and_ignore_task(todolist_id, 3, 2)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=3, name_1="buy eggs", index_2=4, name_2="buy bread")

    app.choose_and_ignore_task(todolist_id, 3, 4)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=3, name="buy eggs")

    app.close_item(todolist_id, 3)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=4, name_2="buy bread")

    app.choose_and_ignore_task(todolist_id, 2, 4)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=2, name="buy water")

    app.close_item(todolist_id, 2)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=4, name_2="buy bread")

    app.choose_and_ignore_task(todolist_id, 4, 1)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=4, name="buy bread")

    app.close_item(todolist_id, 4)

    actual = app.which_task(todolist_id)
    assert actual == DoTheTask(index=1, name="buy milk")

    app.close_item(todolist_id, 1)

    actual = app.which_task(todolist_id)
    assert actual == NothingToDo()

### -----
