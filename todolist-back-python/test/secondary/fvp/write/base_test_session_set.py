from abc import ABC, abstractmethod
from collections import OrderedDict

import pytest

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskKey
from test.fixture import a_task_key
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class BaseTestFvpSessionSet(ABC):
    def test_by(self, sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0)}))
        self.feed(expected)
        assert sut.by() == expected

    @staticmethod
    def test_by_when_no_data(sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        assert sut.by() == expected


    @staticmethod
    def test_save_one_element(sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0), a_task_key(3): a_task_key(0)}))
        sut.save(expected)
        assert sut.by() == expected

    @staticmethod
    def test_update_element(sut: FvpSessionSetPort) -> None:
        initial = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0), a_task_key(3): a_task_key(0)}))
        sut.save(initial)
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0)}))
        sut.save(expected)
        assert sut.by() == expected

    @abstractmethod
    def feed(self, snapshot: FvpSnapshot) -> None:
        pass

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> FvpSessionSetPort:
        return dependencies.get_adapter(FvpSessionSetPort)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()

