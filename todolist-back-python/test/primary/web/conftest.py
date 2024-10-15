import bottle
import pytest
from faker import Faker
from webtest import TestApp

from hexagon.fvp.aggregate import Task, FinalVersionPerfected
from hexagon.fvp.read.which_task import TaskFilter, WhichTask
from hexagon.todolist.aggregate import TodolistSetPort, Todolist
from hexagon.todolist.write.open_task import TaskKeyGeneratorPort, OpenTask
from primary.controller.read.todolist import TodolistPort
from primary.controller.write.dependencies import Dependencies, inject_use_cases
from primary.web.pages import bottle_app, bottle_config
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
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


# todo : move in a single file
class TodolistForTest(WhichTask.Port.Todolist):
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        print("----", self._todolist_set.by(task_filter.todolist_name))
        return [Task(id=task.key.value, name=task.name) for task in self._todolist_set.by(task_filter.todolist_name).value.tasks]



@pytest.fixture
def todolist(todolist_set: TodolistSetPort) -> WhichTask.Port.Todolist:
    return TodolistForTest(todolist_set)

@pytest.fixture
def test_dependencies(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorPort, todolist: WhichTask.Port.Todolist) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = dependencies.feed_adapter(Todolist.Port.TodolistSet, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(OpenTask.Port.TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask.Port.Todolist, lambda _: todolist)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected.Port.SessionSet, lambda _: FvpSessionSetForTest())
    return dependencies