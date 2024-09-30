import pytest

from domain.presentation import ItemPresentation
from domain.todo.todoapp import TodoApp


def a_task(index, name, done=False):
    return ItemPresentation(index=index, name=name, done=done)


def test_register_todolist():
    app = TodoApp()
    app.start_todolist("my todolist")

    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.Started" in notifications[0].topic


@pytest.mark.parametrize("task", ["buy milk", "buy eggs"])
def test_add_first_task(task):
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, task)

    assert app.get_open_items(todolist_id) == [a_task(index=1, name=task)]
    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.ItemAdded" in notifications[1].topic


@pytest.mark.parametrize("item", ["buy milk", "buy eggs"])
def test_add_second_item(item):
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, item)

    assert app.get_open_items(todolist_id) == [a_task(index=1, name="buy water"),
                                               a_task(index=2, name=item)]
    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.ItemAdded" in notifications[2].topic


def test_open_todolist():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")

    todolist_id = app.open_todolist("my todolist")

    assert app.get_open_items(todolist_id) == [a_task(index=1, name="buy water")]


def test_reword_task():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.reword_item(todolist_id, 1, "buy egg")

    assert app.get_open_items(todolist_id) == [a_task(index=1, name="buy egg")]


def test_open_todolist_when_two():
    app = TodoApp()
    todolist_id = app.start_todolist("first todolist")
    app.add_item(todolist_id, "buy water")

    todolist_id = app.start_todolist("second todolist")
    app.add_item(todolist_id, "buy milk")

    todolist_id = app.open_todolist("first todolist")
    assert app.get_open_items(todolist_id) == [a_task(index=1, name="buy water")]

    todolist_id = app.open_todolist("second todolist")
    assert app.get_open_items(todolist_id) == [a_task(index=1, name="buy milk")]


def test_close_item():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy eggs")

    app.close_item(todolist_id, 2)

    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.ItemClosed" in notifications[4].topic

    assert app.get_open_items(todolist_id) == [
        a_task(index=1, name="buy water"),
        a_task(index=3, name="buy eggs")]


def test_all_items():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy eggs")
    app.close_item(todolist_id, 2)

    assert app.all_tasks(todolist_id) == [
        a_task(index=1, name="buy water", done=False),
        a_task(index=2, name="buy milk", done=True),
        a_task(index=3, name="buy eggs", done=False)]


@pytest.mark.parametrize("task_id, expected", [
    (2, a_task(index=2, name="buy milk", done=True)),
    (3, a_task(index=3, name="buy eggs", done=False))
])
def test_read_item(task_id, expected):
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, "buy milk")
    app.add_item(todolist_id, "buy eggs")
    app.close_item(todolist_id, 2)

    assert app.get_task(todolist_id, task_id) == expected