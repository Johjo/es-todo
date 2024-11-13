from dataclasses import replace

import pytest

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
from test.fixture import TodolistFaker, TodolistBuilder


class BaseTestTodolistSetRead:
    def test_read_task_by(self, sut: TodolistSetReadPort, fake: TodolistFaker):
        expected_task = fake.a_task()
        todolist = fake.a_todolist().having(tasks=[fake.a_task(), expected_task, fake.a_task()])
        self.feed_todolist(todolist)

        assert sut.task_by(todolist.name, expected_task.to_key()) == expected_task.to_task()

    def test_read_all_by_name(self, sut: TodolistSetReadPort, fake: TodolistFaker):
        todolist_1 = fake.a_todolist()
        todolist_2 = fake.a_todolist()
        todolist_3 = fake.a_todolist()
        self.feed_todolist(todolist_1)
        self.feed_todolist(todolist_2)
        self.feed_todolist(todolist_3)

        assert sut.all_by_name() == [todolist_1.to_name(), todolist_2.to_name(), todolist_3.to_name()]

    def test_read_counts_by_context(self, sut: TodolistSetReadPort, fake: TodolistFaker):
        todolist = fake.a_todolist().having(tasks=[fake.a_task().having(name="title #context1 #context2"),
                                                   fake.a_task().having(name="#Con_Text3 title #context2"),
                                                   fake.a_task().having(name="@ConText4 title"),
                                                   fake.a_task().having(name="@Con-Text5 title #context2"),
                                                   fake.a_task().having(name="#context1 title #context2",
                                                                        is_open=False),
                                                   ])
        self.feed_todolist(todolist)

        assert sut.counts_by_context(todolist.name) == [("#context1", 1), ("#context2", 3), ("#con_text3", 1),
                                                        ("@context4", 1), ("@con-text5", 1)]

    def test_read_all_tasks(self, sut: TodolistSetReadPort, fake: TodolistFaker):
        expected_tasks = [fake.a_task(), fake.a_task()]
        todolist_1 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        todolist_2 = fake.a_todolist().having(tasks=expected_tasks)
        todolist_3 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        self.feed_todolist(todolist_1)
        self.feed_todolist(todolist_2)
        self.feed_todolist(todolist_3)

        actual = sut.all_tasks(todolist_2.name)
        assert actual == [task.to_task() for task in expected_tasks]

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> TodolistSetReadPort:
        return dependencies.get_adapter(TodolistSetReadPort)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()

    def feed_todolist(self, todolist: TodolistBuilder):
        raise NotImplementedError()
