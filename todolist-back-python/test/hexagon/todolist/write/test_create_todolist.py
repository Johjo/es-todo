import pytest
from expression import Ok, Error, Some, Result

from hexagon.todolist.write.create_todolist import TodolistCreate
from test.hexagon.todolist.fixture import a_todolist_snapshot, TodolistSetForTest


@pytest.mark.parametrize("expected", [
    "my_todolist",
    "other_todolist",
])
def test_create_todolist(expected) -> None:
    todolist_set = TodolistSetForTest()

    response = TodolistCreate(todolist_set).execute(todolist_name=expected)

    assert todolist_set.by(expected) == Some(a_todolist_snapshot(expected))
    assert response == Ok(None)




def test_tell_error_when_create_existing_todolist() -> None:
    todolist_set = TodolistSetForTest()
    todolist_set.feed(a_todolist_snapshot("my_todolist"))

    response: Result[None, None] = TodolistCreate(todolist_set).execute(todolist_name="my_todolist")

    assert response == Error(None)
