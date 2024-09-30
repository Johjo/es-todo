from abc import ABC, abstractmethod
from collections import OrderedDict
from uuid import uuid4, UUID

import pytest

from hexagon.fvp.port import FvpSessionRepository
from test.fixture import an_id
from hexagon.fvp.domain_model import FvpSnapshot


class TestSessionRepositoryContractTesting(ABC):
    def test_by(self, sut: FvpSessionRepository) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]({1: 1, 2: 0}))
        self.feed(expected)
        assert sut.by() == expected

    def test_by_when_no_data(self, sut: FvpSessionRepository) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]())
        assert sut.by() == expected


    def test_save_one_element(self, sut: FvpSessionRepository) -> None:
        expected = FvpSnapshot(OrderedDict[int, int]({an_id(1): 1, an_id(2): 0, an_id(3): 0}))
        sut.save(expected)
        assert sut.by() == expected

    @abstractmethod
    def feed(self, snapshot: FvpSnapshot) -> None:
        pass

    @pytest.fixture
    def sut(self) -> FvpSessionRepository:
        return self._create_sut()

    @abstractmethod
    def _create_sut(self) -> FvpSessionRepository:
        pass
