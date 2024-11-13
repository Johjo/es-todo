import pytest
from expression import Ok, Error

from hexagon.todolist.write.open_task import OpenTaskUseCase
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.fixture import TodolistFaker


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest) -> OpenTaskUseCase:
    return OpenTaskUseCase(todolist_set, task_key_generator)


def test_open_task_when_no_task(sut: OpenTaskUseCase, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist.to_snapshot())
    expected_task = fake.a_task()

    task_key_generator.feed(expected_task.key)

    sut.execute(todolist_name=todolist.name, name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == todolist.having(tasks=[expected_task]).to_snapshot()


def test_open_task_when_one_task(sut, todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    first_task = fake.a_task(1)
    expected_task = fake.a_task(2)

    initial = fake.a_todolist("my_todolist").having(tasks=[first_task])
    todolist_set.feed(initial.to_snapshot())

    task_key_generator.feed(expected_task.key)


    sut.execute(todolist_name="my_todolist", name=expected_task.name)

    actual = todolist_set.by("my_todolist").value
    assert actual == initial.having(tasks=[first_task, expected_task]).to_snapshot()


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


def test_tell_error_when_open_task_for_unknown_todolist(sut, todolist_set):
    response = sut.execute(todolist_name="my_todolist", name="buy the milk")

    assert response == Error("todolist not found")
