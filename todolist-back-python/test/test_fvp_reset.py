import pytest

import primary.controller.read.which_task
from domain.presentation import ChooseTheTask, DoTheTask
from domain.todo.todoapp import TodoApp
from test.fixture import a_task_key


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




