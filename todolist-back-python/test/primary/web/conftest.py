import bottle  # type: ignore
import pytest
from bottle import Bottle
from faker import Faker
from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from src.hexagon.todolist.port import TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from src.infra.fvp_memory import FvpMemory
from src.infra.memory import Memory
from src.primary.adapter_in_memory_dependencies import inject_adapter_in_memory
from src.primary.controller.read.final_version_perfected import CalendarPort
from src.primary.controller.use_case_dependencies import inject_use_cases
from src.primary.controller.write.todolist import DateTimeProviderPort
from src.primary.web.pages import bottle_app, bottle_config
from src.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest, DateTimeProviderForTest
from ._test_double.calendar_for_test import _CalendarForTest


@pytest.fixture
def web_app() -> Bottle:
    bottle.debug(True)
    bottle.TEMPLATE_PATH.insert(0, "../views")
    return bottle_app


@pytest.fixture
def app(web_app: Bottle) -> TestApp:
    return TestApp(web_app)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


@pytest.fixture
def app_dependencies() -> Dependencies:
    bottle_config.dependencies = inject_use_cases(bottle_config.dependencies)
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def datetime_provider() -> DateTimeProviderForTest:
    return DateTimeProviderForTest()


@pytest.fixture
def fvp_memory() -> FvpMemory:
    return FvpMemory()

@pytest.fixture
def memory() -> Memory:
    return Memory()

@pytest.fixture
def calendar() -> _CalendarForTest:
    return _CalendarForTest()


@pytest.fixture
def dependencies(memory: Memory, fvp_memory: FvpMemory, calendar: _CalendarForTest, datetime_provider: DateTimeProviderForTest,
                      task_key_generator: OpenTask_Port_TaskKeyGenerator) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = inject_adapter_in_memory(dependencies)
    dependencies = dependencies.feed_infrastructure(Memory, lambda _: memory)
    dependencies = dependencies.feed_infrastructure(FvpMemory, lambda _: fvp_memory)

    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(CalendarPort, lambda _: calendar)
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, lambda _: datetime_provider)

    return dependencies

