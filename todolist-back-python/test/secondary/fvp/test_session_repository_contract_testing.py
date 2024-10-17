from abc import ABC, abstractmethod
from collections import OrderedDict
from uuid import uuid4, UUID

import pytest

from test.fixture import an_id
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class TestSessionRepositoryContractTesting(ABC):
    def test_by(self, sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]({1: 1, 2: 0}))
        self.feed(expected)
        assert sut.by() == expected

    def test_by_when_no_data(self, sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]())
        assert sut.by() == expected


    def test_save_one_element(self, sut: FvpSessionSetPort) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]({1: 1, 2: 0, 3: 0}))
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
