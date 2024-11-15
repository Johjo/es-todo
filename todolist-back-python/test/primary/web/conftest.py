import bottle  # type: ignore
import pytest
from faker import Faker
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TodolistPort as WhichTask_Port_Todolist
from hexagon.todolist.port import TodolistSetPort as Todolist_Port_TodolistSet, \
    TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from infra.memory import Memory
from primary.controller.dependencies import inject_use_cases
from primary.controller.read.todolist import TodolistSetReadPort, TaskFilter
from primary.web.pages import bottle_app, bottle_config
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.secondary.fvp.read.which_task.test_todolist_memory import TodolistMemory


@pytest.fixture
def web_app():
    bottle.debug(True)
    bottle.TEMPLATE_PATH.insert(0, "../views")
    return bottle_app


@pytest.fixture
def app(web_app) -> TestApp:
    return TestApp(web_app)


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


@pytest.fixture
def app_dependencies() -> Dependencies:
    bottle_config.dependencies = inject_use_cases(bottle_config.dependencies)
    return inject_use_cases(Dependencies.create_empty())


@pytest.fixture
def task_key_generator():
    return TaskKeyGeneratorForTest()


@pytest.fixture
def fvp_session_set() -> FvpSessionSetForTest:
    return FvpSessionSetForTest()

@pytest.fixture
def memory() -> Memory:
    return Memory()


@pytest.fixture
def test_dependencies(memory: Memory, task_key_generator: OpenTask_Port_TaskKeyGenerator, fvp_session_set: FvpSessionSetForTest) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = dependencies.feed_infrastructure(Memory, lambda _: memory)
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, TodolistSetInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, TodolistMemory.factory)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, lambda _: fvp_session_set)
    return dependencies
