from datetime import datetime, date, timedelta

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Some
from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskExecutionDate
from src.infra.memory import Memory
from src.primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest, DateTimeProviderForTest
from test.fixture import TodolistFaker
from test.primary.web.fixture import CleanResponse, BASE_URL, header_with_good_authentication


def test_postpone_task(memory: Memory, datetime_provider: DateTimeProviderForTest, task_key_generator : TaskKeyGeneratorForTest, dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    # GIVEN
    bottle_config.dependencies = dependencies
    initial_task = fake.a_task()
    today = fake.a_datetime()
    datetime_provider.feed(today)
    tomorrow = today + timedelta(days=1)
    expected_task = initial_task.having(execution_date=Some(TaskExecutionDate(tomorrow.date())))

    todolist = fake.a_todolist().having(tasks=(initial_task,))
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())

    # WHEN
    response = app.post(f'{BASE_URL}/{todolist.name}/item/{expected_task.key}/tomorrow', headers=header_with_good_authentication())

    # THEN
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
    assert memory.by(user_key="test@mail.fr", todolist_name=todolist.name).value == todolist.having(tasks=[expected_task]).to_snapshot()



