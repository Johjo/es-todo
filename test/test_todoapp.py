import pytest

from domain.todoapp import TodoApp, Item


def test_register_todolist():
    app = TodoApp()
    app.start_todolist("my todolist")

    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.Started" in notifications[0].topic


@pytest.mark.parametrize("item", ["buy milk", "buy eggs"])
def test_add_first_item(item):
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, item)

    assert app.get_open_items(todolist_id) == [Item(index=1, name=item)]
    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.ItemAdded" in notifications[1].topic


@pytest.mark.parametrize("item", ["buy milk", "buy eggs"])
def test_add_second_item(item):
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")
    app.add_item(todolist_id, item)

    assert app.get_open_items(todolist_id) == [Item(index=1, name="buy water"), Item(index=2, name=item)]
    notifications = app.notification_log.select(start=1, limit=10)
    assert "TodoList.ItemAdded" in notifications[2].topic


def test_open_todolist():
    app = TodoApp()
    todolist_id = app.start_todolist("my todolist")
    app.add_item(todolist_id, "buy water")

    todolist_id = app.open_todolist("my todolist")

    assert app.get_open_items(todolist_id) == [Item(index=1, name="buy water")]


def test_open_todolist_when_two():
    app = TodoApp()
    todolist_id = app.start_todolist("first todolist")
    app.add_item(todolist_id, "buy water")

    todolist_id = app.start_todolist("second todolist")
    app.add_item(todolist_id, "buy milk")

    todolist_id = app.open_todolist("first todolist")
    assert app.get_open_items(todolist_id) == [Item(index=1, name="buy water")]

    todolist_id = app.open_todolist("second todolist")
    assert app.get_open_items(todolist_id) == [Item(index=1, name="buy milk")]
