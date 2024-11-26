from datetime import date

import pytest
from dateutil.utils import today

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort, TaskFilter, Include, Exclude, Word
from test.fixture import TodolistFaker, TodolistBuilder


class BaseTestTodolistSetRead:
    def test_read_task_by(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_task = fake.a_task()
        todolist = fake.a_todolist().having(tasks=[fake.a_task(), expected_task, fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        assert sut.task_by(todolist.name, expected_task.to_key()) == expected_task.to_presentation()

    def test_read_task_having_execution_date(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_task = fake.a_task().having(execution_date=today().date())
        todolist = fake.a_todolist().having(tasks=[fake.a_task(), expected_task, fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        assert sut.task_by(todolist.name, expected_task.to_key()) == expected_task.to_presentation()

    def test_read_all_by_name(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        todolist_1 = fake.a_todolist()
        todolist_2 = fake.a_todolist()
        todolist_3 = fake.a_todolist()
        self.feed_todolist(user_key=current_user, todolist=todolist_1)
        self.feed_todolist(user_key=current_user, todolist=todolist_2)
        self.feed_todolist(user_key=current_user, todolist=todolist_3)

        assert sut.all_by_name() == sorted([todolist_1.to_name(), todolist_2.to_name(), todolist_3.to_name()])

    def test_read_counts_by_context(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        todolist = fake.a_todolist().having(tasks=[fake.a_task().having(name="title #context1 #context2"),
                                                   fake.a_task().having(name="#Con_Text3 title #context2"),
                                                   fake.a_task().having(name="@ConText4 title"),
                                                   fake.a_task().having(name="@Con-Text5 title #context2"),
                                                   fake.a_task().having(name="#context1 title #context2",
                                                                        is_open=False),
                                                   ])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        assert sut.counts_by_context(todolist.name) == [("#context1", 1), ("#context2", 3), ("#con_text3", 1),
                                                        ("@context4", 1), ("@con-text5", 1)]

    def test_read_all_tasks(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_tasks = [fake.a_task().having(name="#include1 buy the milk"), fake.a_task().having(name="buy the water #include2")]
        todolist_1 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task().having(execution_date=today().date())])
        todolist_2 = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(name="#include1 #exclude2"), fake.a_task().having(name="#include2 #exclude1")])
        todolist_3 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist_1)
        self.feed_todolist(user_key=current_user, todolist=todolist_2)
        self.feed_todolist(user_key=current_user, todolist=todolist_3)

        task_filter = TaskFilter.create(todolist_2.to_name(), Include(Word("#include1")), Include(Word("#include2")), Exclude(Word("#exclude1")), Exclude(Word("#exclude2")))

        actual = sut.all_tasks(task_filter)

        assert actual == [task.to_presentation() for task in expected_tasks]

    def test_read_all_postponed_tasks(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_tasks = [fake.a_task().having(execution_date=date(2018, 10, 17)),
                          fake.a_task().having(execution_date=date(2019, 10, 17)),
                          fake.a_task().having(execution_date=date(2020, 10, 17)),
                          fake.a_task().having(execution_date=date(2021, 11, 23))]
        todolist = fake.a_todolist().having(tasks=[expected_tasks[2], expected_tasks[1], fake.a_task(), expected_tasks[3], fake.a_closed_task(), expected_tasks[0]])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        actual = sut.all_tasks_postponed_task(todolist_name=todolist.to_name())

        assert actual == [task.to_presentation() for task in expected_tasks]

    @pytest.fixture
    def current_user(self, fake: TodolistFaker) -> str:
        return fake.a_user_key()

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> TodolistSetReadPort:
        return dependencies.get_adapter(TodolistSetReadPort)

    @pytest.fixture
    def dependencies(self, current_user: str) -> Dependencies:
        raise NotImplementedError() # pragma: no cover

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder):
        raise NotImplementedError() # pragma: no cover
