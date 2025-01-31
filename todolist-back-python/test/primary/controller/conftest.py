import pytest
from faker import Faker

from src.dependencies import Dependencies
from src.infra.fvp_memory import FvpMemory
from src.infra.memory import Memory
from src.primary.adapter_in_memory_dependencies import inject_adapter_in_memory
from src.primary.controller.use_case_dependencies import inject_use_cases
from src.primary.infrastructure_in_memory_dependencies import inject_infrastructure_in_memory
from src.shared.const import USER_KEY
from test.fixture import TodolistFaker


@pytest.fixture
def dependencies(memory: Memory, fvp_memory: FvpMemory) -> Dependencies:
    dependencies = inject_use_cases(Dependencies.create_empty())
    dependencies = inject_adapter_in_memory(dependencies)
    dependencies = inject_infrastructure_in_memory(dependencies=dependencies, memory=memory, fvp_memory=fvp_memory)
    dependencies = dependencies.feed_data(data_name=USER_KEY, value="any user")
    return dependencies


@pytest.fixture
def memory() -> Memory:
    return Memory()


@pytest.fixture
def fvp_memory() -> FvpMemory:
    return FvpMemory()

@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
