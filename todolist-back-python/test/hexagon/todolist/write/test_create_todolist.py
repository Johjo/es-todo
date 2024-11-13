import pytest
from expression import Ok, Error, Result

from hexagon.todolist.write.create_todolist import TodolistCreate
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest

@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()

@pytest.fixture
def sut(todolist_set: TodolistSetForTest) -> TodolistCreate:
    return TodolistCreate(todolist_set)


def test_create_todolist(sut: TodolistCreate, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
    # GIVEN
    expected_todolist = fake.a_todolist()
    todolist_set.feed_nothing(expected_todolist.to_name())

    #WHEN
    response = sut.execute(todolist_name=expected_todolist.to_name())

    # THEN
    assert todolist_set.by(expected_todolist.name).value == expected_todolist.to_snapshot()
    assert response == Ok(None)


def test_tell_error_when_create_existing_todolist(sut: TodolistCreate, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
    # GIVEN
    existing_todolist = fake.a_todolist()
    todolist_set.feed(existing_todolist)

    # WHEN
    response = sut.execute(todolist_name=existing_todolist.to_name())

    # THEN
    assert response == Error(None)
