import pytest
from expression import Ok, Error

from src.hexagon.shared.type import TaskName
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest, TodolistSetForTest


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> OpenTaskUseCase:
    return OpenTaskUseCase(todolist_set, task_key_generator)


def test_open_task_when_no_task(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()

    task_key_generator.feed(expected_task.to_key())

    sut.execute(todolist_name=todolist.to_name(), name=expected_task.to_name())

    actual = todolist_set.by(todolist.name).value

    assert actual == todolist.having(tasks=[expected_task]).to_snapshot()


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    first_task = fake.a_task(1)
    expected_task = fake.a_task(2)

    todolist = fake.a_todolist().having(tasks=[first_task])
    todolist_set.feed(todolist)

    task_key_generator.feed(expected_task.to_key())


    sut.execute(todolist_name=todolist.to_name(), name=expected_task.name)

    actual = todolist_set.by(todolist.to_name()).value
    assert actual == todolist.having(tasks=[first_task, expected_task]).to_snapshot()


def test_tell_ok_when_open_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    # data
    todolist = fake.a_todolist()
    open_task = fake.a_task()

    # given
    todolist_set.feed(todolist)
    task_key_generator.feed(open_task.to_key())

    # when
    response = sut.execute(todolist_name=todolist.to_name(), name=open_task.to_name())

    # then
    assert response == Ok(None)


def test_tell_error_when_open_task_for_unknown_todolist(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest, fake: TodolistFaker):
    # GIVEN
    unknown_todolist = fake.a_todolist()
    todolist_set.feed_nothing(unknown_todolist.to_name())

    # WHEN
    response = sut.execute(todolist_name=unknown_todolist.to_name(), name=TaskName("buy the milk"))

    # THEN
    assert response == Error("todolist not found")

