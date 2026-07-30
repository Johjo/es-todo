import pytest

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from infra.fvp_memory import FvpMemory
from secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from shared.const import USER_KEY
from test.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


class TestFvpSessionSetInMemory(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self) -> None:
        self._fvp_memory = FvpMemory()

    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        self._fvp_memory.feed(user_key=user_key, snapshot=snapshot)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        dep = Dependencies.create_empty()
        dep = dep.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
        dep = dep.feed_infrastructure(FvpMemory, lambda _: self._fvp_memory)
        dep = dep.feed_data(data_name=USER_KEY, value="any user")
        return dep
