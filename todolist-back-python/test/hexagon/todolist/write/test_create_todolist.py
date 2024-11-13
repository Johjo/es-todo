import pytest
from expression import Ok, Error, Result

from hexagon.todolist.write.create_todolist import TodolistCreate
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.mark.parametrize("expected", [
    "my_todolist",
    "other_todolist",
])
def test_create_todolist(expected, fake: TodolistFaker) -> None:
    expected_todolist = fake.a_todolist(expected)
    todolist_set = TodolistSetForTest()

    response = TodolistCreate(todolist_set).execute(todolist_name=expected_todolist.name)

    assert todolist_set.by(expected_todolist.name).value == expected_todolist.to_snapshot()
    assert response == Ok(None)


def test_tell_error_when_create_existing_todolist(fake: TodolistFaker) -> None:
    # given
    existing_todolist = fake.a_todolist()
    todolist_set = TodolistSetForTest()
    todolist_set.feed(existing_todolist)

    # when
    response: Result[None, None] = TodolistCreate(todolist_set).execute(todolist_name=existing_todolist.to_name())

    # then
    assert response == Error(None)
