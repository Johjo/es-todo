from dataclasses import replace

from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.fixture import TodolistFaker


def test_show_when_no_task(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                           fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(replace(fake.a_todolist_old(), name="my_todolist"))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_one_task(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                            fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(
        replace(fake.a_todolist_old(), name="my_todolist", tasks=[replace(fake.a_task_old(1), name="buy the milk")]))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_two_tasks(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                            fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(
        replace(fake.a_todolist_old(), name="my_todolist", tasks=[
            replace(fake.a_task_old(1), name="buy the milk"), replace(fake.a_task_old(2), name="buy the water")]))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
