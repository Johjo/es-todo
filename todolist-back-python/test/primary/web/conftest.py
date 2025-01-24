import bottle  # type: ignore
import pytest
from bottle import Bottle
from faker import Faker
from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from src.hexagon.fvp.read.which_task import TodolistPort as WhichTask_Port_Todolist
from src.hexagon.todolist.port import TodolistSetPort as Todolist_Port_TodolistSet, \
    TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from src.infra.memory import Memory
from src.primary.controller.use_case_dependencies import inject_use_cases
from src.primary.controller.read.final_version_perfected import CalendarPort
from src.primary.controller.read.todolist import TodolistSetReadPort
from src.primary.controller.write.todolist import DateTimeProviderPort
from src.primary.web.pages import bottle_app, bottle_config
from src.secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory
from src.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from src.secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory
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
def fvp_session_set() -> FvpSessionSetInMemory:
    return FvpSessionSetInMemory()

@pytest.fixture
def memory() -> Memory:
    return Memory()

@pytest.fixture
def calendar() -> _CalendarForTest:
    return _CalendarForTest()


@pytest.fixture
def test_dependencies(memory: Memory, calendar: _CalendarForTest, datetime_provider: DateTimeProviderForTest,
                      task_key_generator: OpenTask_Port_TaskKeyGenerator,
                      fvp_session_set: FvpSessionSetInMemory) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = dependencies.feed_infrastructure(Memory, lambda _: memory)
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, TodolistSetInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, TodolistInMemory.factory)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, lambda _: fvp_session_set)
    dependencies = dependencies.feed_adapter(CalendarPort, lambda _: calendar)
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, lambda _: datetime_provider)

    return dependencies

