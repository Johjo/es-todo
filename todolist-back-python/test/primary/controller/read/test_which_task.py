from random import randint

import pytest

from hexagon.fvp.domain_model import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.port import FvpSessionRepository
from hexagon.fvp.read.which_task import WhichTaskQueryContract, TaskReader
from primary.controller.read.which_task import DependencyList, which_task
from secondary.fvp.simple_session_repository import SimpleSessionRepository
from test.hexagon.fvp.read.test_which_task import SimpleTaskReader


class WhichTaskQueryForTest(WhichTaskQueryContract):
    def __init__(self) -> None:
        super().__init__()
        self.value: None | NothingToDo | DoTheTask | ChooseTheTask = None

    def feed(self, value: NothingToDo | DoTheTask | ChooseTheTask):
        self.value = value

    def which_task(self) -> NothingToDo | DoTheTask | ChooseTheTask:
        assert self.value is not None, "feed() must be called before which_task()"
        return self.value


class DependencyListForTest(DependencyList):
    def __init__(self, which_task_query=None) -> None:
        super().__init__()
        self._which_task_query: WhichTaskQueryForTest | None = which_task_query

    def task_reader_for_which_task_query(self, todolist_name: str, only_inbox: bool, context: str) -> TaskReader:
        return SimpleTaskReader()

    def fvp_session_repository_for_which_task_query(self) -> FvpSessionRepository:
        return SimpleSessionRepository()

    def which_task_query(self, todolist_name: str, only_inbox: bool, context: str) -> WhichTaskQueryContract:
        if self._which_task_query:
            return self._which_task_query
        return super().which_task_query(todolist_name=todolist_name, only_inbox=only_inbox, context=context)


class TestWhichTaskQueryContractTesting:
    @pytest.fixture
    def which_task_query(self) -> WhichTaskQueryForTest:
        return WhichTaskQueryForTest()

    def test_read_fvp_session_when_nothing_to_do(self, which_task_query):
        dependencies = DependencyListForTest(which_task_query=which_task_query)
        session = NothingToDo()
        which_task_query.feed(session)

        actual = which_task(dependencies=dependencies, context=None, only_inbox=None, todolist_name=None)
        expected = {"fvpTasks": []}

        assert actual == expected

    def test_read_fvp_session_when_one_task_to_do(self, which_task_query):
        dependencies = DependencyListForTest(which_task_query=which_task_query)
        session = DoTheTask(id=randint(1, 100), name="buy the milk #course")
        which_task_query.feed(session)

        actual = which_task(dependencies=dependencies, context=None, only_inbox=None, todolist_name=None)
        expected = {"fvpTasks": [{"id": session.id, "name": session.name}]}

        assert actual == expected

    def test_read_fvp_session_when_two_tasks_to_choose(self, which_task_query):
        dependencies = DependencyListForTest(which_task_query=which_task_query)
        session = ChooseTheTask(id_1=randint(1, 100), name_1="buy the milk",
                                id_2=randint(1, 100), name_2="clean the table")
        which_task_query.feed(session)

        actual = which_task(dependencies=dependencies, context=None, only_inbox=None, todolist_name=None)
        expected = {"fvpTasks": [
            {"id": session.id_1, "name": session.name_1},
            {"id": session.id_2, "name": session.name_2}]
        }

        assert actual == expected


class TestWhichTaskQueryIntegration:
    def test_read_fvp_session_when_nothing_to_do(self):
        dependencies = DependencyListForTest()

        actual = which_task(dependencies=dependencies, context=None, only_inbox=None, todolist_name=None)
        expected = {"fvpTasks": []}

        assert actual == expected