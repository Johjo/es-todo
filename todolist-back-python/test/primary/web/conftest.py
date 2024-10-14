import bottle
import pytest
from faker import Faker
from webtest import TestApp

from hexagon.todolist.aggregate import TodolistSetPort
from hexagon.todolist.write.open_task import TaskKeyGeneratorPort
from primary.controller.write.dependencies import Dependencies, inject_use_cases
from primary.web.pages import bottle_app, bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, TodolistSetForTest
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest


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
def todolist_set():
    return TodolistSetForTest()

@pytest.fixture
def task_key_generator():
    return TaskKeyGeneratorForTest()

@pytest.fixture
def test_dependencies(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorPort) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)

    return dependencies