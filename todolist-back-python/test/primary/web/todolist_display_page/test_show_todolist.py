from datetime import date

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web._test_double.calendar_for_test import _CalendarForTest


def test_show_when_no_task(memory:Memory, calendar: _CalendarForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    memory.save(fake.a_todolist(name="my_todolist").to_snapshot())
    calendar.feed_today(fake.a_date())
    response = app.get('/any_user/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_one_task(memory:Memory, calendar: _CalendarForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    calendar.feed_today(fake.a_date())
    memory.save(fake.a_todolist(name="my_todolist").having(tasks=[fake.a_task(1).having(name="buy the milk")]).to_snapshot())

    response = app.get('/any_user/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_task_has_execution_date(memory:Memory, calendar: _CalendarForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    calendar.feed_today(date(2024, 5, 17))
    memory.save(fake.a_todolist(name="my_todolist").having(
        tasks=[fake.a_task(1).having(name="buy the milk", execution_date=date(2023, 10, 19))]).to_snapshot())

    response = app.get('/any_user/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_two_tasks(memory:Memory, calendar: _CalendarForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    calendar.feed_today(fake.a_date())
    memory.save(fake.a_todolist().having(
        name="my_todolist",
        tasks=[fake.a_task(1).having(name="buy the milk"), fake.a_task(2).having(name="buy the water")]).to_snapshot())

    response = app.get('/any_user/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
