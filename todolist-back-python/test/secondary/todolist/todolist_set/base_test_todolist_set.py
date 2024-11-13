import pytest
from expression import Nothing, Some
from faker import Faker

from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from test.fixture import TodolistFaker, TodolistBuilder


class BaseTestTodolistSet:
    def test_get_by_when_one_todolist(self, sut: TodolistSetPort, fake: TodolistFaker):
        # given
        expected_todolist = fake.a_todolist()
        self.feed_todolist(todolist=expected_todolist)

        # when
        actual = sut.by(expected_todolist.to_name())

        # then
        assert actual.value == expected_todolist.to_snapshot()

    def test_get_by_when_two_todolist(self, sut: TodolistSetPort, fake: TodolistFaker):
        # given
        todolist_one = fake.a_todolist()
        todolist_two = fake.a_todolist()
        self.feed_todolist(todolist_one)
        self.feed_todolist(todolist_two)

        # when / then
        assert sut.by(todolist_one.name).value == todolist_one.to_snapshot()
        assert sut.by(todolist_two.name).value == todolist_two.to_snapshot()

    def test_get_by_when_todolist_has_tasks(self, sut: TodolistSetPort, fake: TodolistFaker):
        # given
        expected_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        self.feed_todolist(fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()]))
        self.feed_todolist(expected_todolist)

        #when
        actual = sut.by(expected_todolist.name)

        # then
        assert actual == Some(expected_todolist.to_snapshot())

    @staticmethod
    def test_get_when_todolist_does_not_exist(sut: TodolistSetPort, fake: TodolistFaker):
        # given
        unknown_todolist = fake.a_todolist()

        # when
        actual = sut.by(unknown_todolist.to_name())

        # then
        assert actual == Nothing

    @staticmethod
    def test_insert_todolist(sut: TodolistSetPort, fake: TodolistFaker):
        # given
        expected_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

        # when
        sut.save_snapshot(expected_todolist.to_snapshot())

        # then
        assert sut.by(expected_todolist.name).value == expected_todolist.to_snapshot()

    @staticmethod
    def test_update_todolist(sut: TodolistSetPeewee, fake: TodolistFaker):
        # given
        initial_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        sut.save_snapshot(initial_todolist.to_snapshot())

        # when
        expected_todolist = initial_todolist.having(tasks=[fake.a_task(), fake.a_task()])
        sut.save_snapshot(expected_todolist.to_snapshot())

        # then
        assert sut.by(expected_todolist.name).value == expected_todolist.to_snapshot()

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> TodolistSetPort:
        return dependencies.get_adapter(TodolistSetPort)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()

    def feed_todolist(self, todolist: TodolistBuilder) -> None:
        raise NotImplementedError()

    @pytest.fixture
    def fake(self) -> TodolistFaker:
        return TodolistFaker(Faker())
