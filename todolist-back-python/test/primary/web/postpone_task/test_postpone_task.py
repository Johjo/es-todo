from datetime import datetime

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from expression import Some
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.shared.type import TaskExecutionDate
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.fixture import TodolistFaker
from test.primary.web.fixture import CleanResponse


def test_postpone_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    initial_task = fake.a_task()
    today = datetime.today().date()
    expected_task = initial_task.having(execution_date=Some(TaskExecutionDate(today)))

    todolist = fake.a_todolist().having(tasks=(initial_task,))
    memory.save(todolist.to_snapshot())

    response = app.post(f'/todo/{todolist.name}/item/{expected_task.key}/postpone', {"execution_date": str(today)})
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
    assert memory.by(todolist.name).value == todolist.having(tasks=[expected_task]).to_snapshot()


def test_display_error_if_date_is_invalid(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    initial_task = fake.a_task(1).having(name="buy the milk")

    todolist = fake.a_todolist("todolist").having(tasks=[initial_task])

    memory.save(todolist.to_snapshot())

    response = app.post(f'/todo/{todolist.name}/item/{initial_task.key}/postpone', {"execution_date": ""})

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())



