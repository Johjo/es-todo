from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.infra.memory import Memory
from src.primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse, BASE_URL, header_with_good_authentication


def test_reword_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    # given
    bottle_config.dependencies = dependencies
    initial_task = fake.a_task()
    expected_task = initial_task.having(name="reworded")

    todolist = fake.a_todolist().having(tasks=[initial_task])
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())

    # when
    response = app.post(f'{BASE_URL}/{todolist.to_name()}/item/{expected_task.to_key()}/reword', {"new_name": expected_task.to_name()}, headers=header_with_good_authentication())

    # then
    assert expected_task.to_snapshot() in memory.by(user_key="test@mail.fr", todolist_name=todolist.to_name()).value.tasks
    assert CleanResponse(response).location() == f"/todo/{todolist.to_name()}"
    assert response.status_code == 302

