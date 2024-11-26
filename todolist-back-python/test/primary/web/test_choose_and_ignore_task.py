
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.fixture import TodolistFaker
from test.primary.web.fixture import CleanResponse, BASE_URL


def test_choose_and_ignore_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    # given
    bottle_config.dependencies = test_dependencies
    task_1 = fake.a_task().having(name="buy the milk")
    task_2 = fake.a_task().having(name="buy the water")

    todolist = fake.a_todolist().having(tasks=[task_1, task_2])
    memory.save(user_key="todo@user.com", todolist=todolist.to_snapshot())

    # when
    response = app.post(f'{BASE_URL}/{todolist.to_name()}/item/choose/{task_1.to_key()}/ignore/{task_2.to_key()}')

    # then
    assert CleanResponse(response).location() == f"/todo/{todolist.to_name()}"
    assert response.status_code == 302

