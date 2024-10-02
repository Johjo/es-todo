import pytest

import primary.controller.read.which_task
from domain.presentation import ChooseTheTask, DoTheTask
from domain.todo.todoapp import TodoApp


def test_can_do_again_choosing_after_reset():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")
    app.add_item(todolist_id, "buy bread")
    app.choose_and_ignore_task(todolist_id, 2, 1)
    app.choose_and_ignore_task(todolist_id, 3, 2)
    app.choose_and_ignore_task(todolist_id, 3, 4)

    app.reset_fvp_algorithm(todolist_id)

    actual = app.which_task(todolist_id)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")


@pytest.mark.skip(reason="not implemented")
def test_acceptance_reset_algorithm():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")

    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy eggs")
    app.add_item(todolist_id, "buy bread")

    prioritize_tasks(app, todolist_id)

    app.reset_fvp_algorithm(todolist_id)

    prioritize_tasks(app, todolist_id)


def prioritize_tasks(app, todolist_id):
    actual = primary.controller.read.which_task_old.which_task_old(todolist_id, None, None, None)
    assert actual == ChooseTheTask(index_1=1, name_1="buy milk", index_2=2, name_2="buy water")
    app.choose_and_ignore_task(todolist_id, 2, 1)
    actual = primary.controller.read.which_task_old.which_task_old(todolist_id, None, None, None)
    assert actual == ChooseTheTask(index_1=2, name_1="buy water", index_2=3, name_2="buy eggs")
    app.choose_and_ignore_task(todolist_id, 3, 2)
    actual = primary.controller.read.which_task_old.which_task_old(todolist_id, None, None, None)
    assert actual == ChooseTheTask(index_1=3, name_1="buy eggs", index_2=4, name_2="buy bread")
    app.choose_and_ignore_task(todolist_id, 3, 4)
    actual = primary.controller.read.which_task_old.which_task_old(todolist_id, None, None, None)
    assert actual == DoTheTask(index=3, name="buy eggs")




