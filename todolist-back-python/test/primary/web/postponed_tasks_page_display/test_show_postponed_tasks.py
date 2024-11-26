from datetime import date

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web._test_double.calendar_for_test import _CalendarForTest
from test.primary.web.fixture import header_with_good_authentication


def test_show_postponed_tasks(memory: Memory, calendar: _CalendarForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    calendar.feed_today(date(2019,10, 13))
    todolist = fake.a_todolist(name="my_todolist").having(tasks=[fake.a_task(1).having(name="buy the milk", execution_date=date(2020,10, 13)), fake.a_task(2).having(name="buy the water", execution_date=date(2020,10, 14))])
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())
    response = app.get('/any_user/todo/my_todolist/calendar', headers=header_with_good_authentication())

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
