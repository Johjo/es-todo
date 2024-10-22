import pytest
from faker import Faker
from peewee import Database

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from test.fixture import TodolistFaker
from test.secondary.todolist.peewee.conftest import peewee_database


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


@pytest.fixture
def dependencies(peewee_database: Database) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistPeewee.factory)
    dependencies = dependencies.feed_infrastructure(Database, lambda _: peewee_database)
    return dependencies


@pytest.fixture
def sut(dependencies: Dependencies) -> TodolistPeewee:
    return dependencies.get_adapter(TodolistPort)


def test_should_list_open_tasks(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task(), fake.a_task()]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(is_open=False)])
    another_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())
    TodolistSetPeewee(database=peewee_database).save_snapshot(another_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name)) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]


def test_should_list_only_task_having_one_included_context(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"), fake.a_task().having(name="buy the water #supermarket")]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket",))) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]


def test_should_list_only_task_having_any_included_context(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"), fake.a_task().having(name="jogging #sport")]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket", "#sport"))) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]


def test_should_not_list_task_having_any_excluded_context(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"), ]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket #sport")])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket",), exclude_context=("#sport",))) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]


def test_should_include_only_task_matching_full_context(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task().having(name="become #super man"), ]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket")])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=("#super",), exclude_context=())) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]

def test_should_exclude_only_task_matching_full_context(sut: TodolistPeewee, peewee_database: Database, fake: TodolistFaker):
    expected_tasks = [fake.a_task().having(name="buy the water #supermarket"), ]
    expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(name="become #super man")])

    TodolistSetPeewee(database=peewee_database).save_snapshot(expected_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=(), exclude_context=("#super",))) == [
        Task(id=task.key, name=task.name) for task in expected_tasks]



def test_should_no_task_when_todolist_does_not_exist(sut: TodolistPeewee, peewee_database: Database,
                                                     fake: TodolistFaker):
    unknown_todolist = fake.a_todolist()
    another_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

    TodolistSetPeewee(database=peewee_database).save_snapshot(another_todolist.to_snapshot())

    assert sut.all_open_tasks(TaskFilter(todolist_name=unknown_todolist.name)) == []
