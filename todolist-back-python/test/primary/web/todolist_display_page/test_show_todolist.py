from datetime import datetime

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Option, Nothing, Some  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker


def test_show_when_no_task(memory: Memory, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    memory.save(fake.a_todolist(name="my_todolist").to_snapshot())
    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_one_task(memory: Memory, test_dependencies: Dependencies, app: TestApp,
                            fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    memory.save(fake.a_todolist(name="my_todolist").having(tasks=[fake.a_task(1).having(name="buy the milk")]).to_snapshot())

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_task_has_execution_date(memory: Memory, test_dependencies: Dependencies,
                                           app: TestApp,
                                           fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    memory.save(fake.a_todolist(name="my_todolist").having(
        tasks=[fake.a_task(1).having(name="buy the milk", execution_date=datetime(2023, 10, 19))]).to_snapshot())

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_two_tasks(memory: Memory, test_dependencies: Dependencies, app: TestApp,
                             fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    memory.save(fake.a_todolist().having(
        name="my_todolist",
        tasks=[fake.a_task(1).having(name="buy the milk"), fake.a_task(2).having(name="buy the water")]).to_snapshot())

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
