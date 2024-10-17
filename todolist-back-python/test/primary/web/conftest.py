import bottle  # type: ignore
import pytest
from faker import Faker
from webtest import TestApp  # type: ignore

from hexagon.fvp.read.which_task import TodolistPort as WhichTask_Port_Todolist
from hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from hexagon.fvp.aggregate import Task
from hexagon.fvp.read.which_task import TaskFilter
from hexagon.todolist.port import TodolistSetPort as Todolist_Port_TodolistSet, \
    TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from primary.controller.dependencies import inject_use_cases
from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
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
class TodolistForTest(WhichTask_Port_Todolist):
    def __init__(self, todolist_set: Todolist_Port_TodolistSet):
        self._todolist_set = todolist_set

    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        return [Task(id=task.key.value, name=task.name) for task in self._todolist_set.by(task_filter.todolist_name).value.tasks if task.is_open]



@pytest.fixture
def todolist(todolist_set: Todolist_Port_TodolistSet) -> WhichTask_Port_Todolist:
    return TodolistForTest(todolist_set)

@pytest.fixture
def test_dependencies(todolist_set: TodolistSetForTest, task_key_generator: OpenTask_Port_TaskKeyGenerator, todolist: WhichTask_Port_Todolist) -> Dependencies:
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, lambda _: todolist)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, lambda _: FvpSessionSetForTest())
    return dependencies