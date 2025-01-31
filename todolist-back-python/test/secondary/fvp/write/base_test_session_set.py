from abc import ABC, abstractmethod
from collections import OrderedDict

import pytest
from faker import Faker

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.hexagon.shared.type import TaskKey, UserKey
from test.fixture import a_task_key
from test.hexagon.fvp.read.test_which_task import FvpFaker


class BaseTestFvpSessionSet(ABC):
    def test_by(self, sut: FvpSessionSetPort, fake: FvpFaker) -> None:
        the_user = fake.a_user_key()
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0)}))
        self.feed(user_key=fake.a_user_key(), snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]()))
        self.feed(user_key=the_user, snapshot=expected)
        self.feed(user_key=fake.a_user_key(), snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]()))
        assert sut.by(user_key=the_user) == expected

    @staticmethod
    def test_by_when_no_data(sut: FvpSessionSetPort, fake: FvpFaker) -> None:
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        assert sut.by(user_key=fake.a_user_key()) == expected

    @staticmethod
    def test_save_one_element(sut: FvpSessionSetPort, fake: FvpFaker) -> None:
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0), a_task_key(3): a_task_key(0)}))
        user_key = fake.a_user_key()
        sut.save(user_key=user_key, snapshot=expected)
        assert sut.by(user_key=user_key) == expected

    @staticmethod
    def test_update_element(sut: FvpSessionSetPort, fake: FvpFaker) -> None:
        initial = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0), a_task_key(3): a_task_key(0)}))
        user_key = fake.a_user_key()
        sut.save(user_key=user_key, snapshot=initial)
        expected = FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(1): a_task_key(1), a_task_key(2): a_task_key(0)}))
        sut.save(user_key=user_key, snapshot=expected)
        assert sut.by(user_key=user_key) == expected

    @abstractmethod
    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        pass

    @pytest.fixture
    def sut(self, dependencies: Dependencies) -> FvpSessionSetPort:
        return dependencies.get_adapter(FvpSessionSetPort)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()

    @pytest.fixture()
    def fake(self) -> FvpFaker:
        return FvpFaker(Faker())
