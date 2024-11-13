import pytest
from faker import Faker

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort, TaskFilter
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee
from test.fixture import TodolistFaker, TodolistBuilder


class BaseTestTodolist:
    def test_should_list_open_tasks(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task(), fake.a_task()]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(is_open=False)])
        another_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

        self.feed_todolist(expected_todolist)
        self.feed_todolist(another_todolist)

        assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name)) == [
            Task(id=task.key, name=task.name) for task in expected_tasks]

    def test_should_list_only_task_having_one_included_context(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"),
                          fake.a_task().having(name="buy the water #supermarket")]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

        self.feed_todolist(expected_todolist)

        assert sut.all_open_tasks(
            TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket",))) == [
                   Task(id=task.key, name=task.name) for task in expected_tasks]

    def test_should_list_only_task_having_any_included_context(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"),
                          fake.a_task().having(name="jogging #sport")]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

        self.feed_todolist(expected_todolist)

        assert sut.all_open_tasks(
            TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket", "#sport"))) == [
                   Task(id=task.key, name=task.name) for task in expected_tasks]

    def test_should_not_list_task_having_any_excluded_context(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket #sport")])

        self.feed_todolist(expected_todolist)

        assert sut.all_open_tasks(TaskFilter(todolist_name=expected_todolist.name, include_context=("#supermarket",),
                                             exclude_context=("#sport",))) == [
                   Task(id=task.key, name=task.name) for task in expected_tasks]

    def test_should_include_only_task_matching_full_context(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task().having(name="become #super man"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket")])

        self.feed_todolist(expected_todolist)

        assert sut.all_open_tasks(
            TaskFilter(todolist_name=expected_todolist.name, include_context=("#super",), exclude_context=())) == [
                   Task(id=task.key, name=task.name) for task in expected_tasks]

    def test_should_exclude_only_task_matching_full_context(self, sut: TodolistPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task().having(name="buy the water #supermarket"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="become #super man")])

        self.feed_todolist(expected_todolist)

        assert sut.all_open_tasks(
            TaskFilter(todolist_name=expected_todolist.name, include_context=(), exclude_context=("#super",))) == [
                   Task(id=task.key, name=task.name) for task in expected_tasks]

    @staticmethod
    def test_should_no_task_when_todolist_does_not_exist(sut: TodolistPort, fake: TodolistFaker):
        unknown_todolist = fake.a_todolist()
        assert sut.all_open_tasks(TaskFilter(todolist_name=unknown_todolist.name)) == []

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        raise NotImplementedError()

    @pytest.fixture
    def fake(self) -> TodolistFaker:
        return TodolistFaker(Faker())

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> TodolistPeewee:
        return dependencies.get_adapter(TodolistPort)
