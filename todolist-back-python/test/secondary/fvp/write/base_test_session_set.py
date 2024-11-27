from abc import ABC, abstractmethod
from collections import OrderedDict

import pytest

from hexagon.shared.type import TaskKey
from test.fixture import a_task_key
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class BaseTestSessionSet(ABC):
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
    def sut(self) -> FvpSessionSetPort:
        return self._create_sut()

    @abstractmethod
    def _create_sut(self) -> FvpSessionSetPort:
        pass
