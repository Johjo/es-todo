from dataclasses import replace

import bottle  # type: ignore
import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter
from faker import Faker
from webtest import TestApp, TestResponse  # type: ignore

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.dependencies import inject_use_cases, Dependencies
from primary.web.pages import bottle_app, bottle_config
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


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

def test_index(app_dependencies: Dependencies, web_app, app: TestApp, fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist_set.feed(replace(fake.a_todolist(), name="1-todolist-1"))
    todolist_set.feed(replace(fake.a_todolist(), name="2-todolist-2"))
    app_dependencies = app_dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    bottle_config.dependencies = app_dependencies
    response = app.get('/')
    print(response.body)
    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
    # which_task_query.feed(ChooseTheTask(id_1=1, name_1="buy the milk", id_2=2, name_2="clean the table"))
    #
    # try:
    #     response: TestResponse = app.get('/rest/todo/anytodolist/which_task')
    # except Exception as e:
    #     print(e)
    #     raise
    #
    # assert response.status == '200 OK'
    # verify(response.body)
