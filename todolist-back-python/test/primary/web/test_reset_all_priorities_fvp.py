from collections import OrderedDict

from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.shared.type import TaskKey
from infra.memory import Memory
from primary.web.pages import bottle_config
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse, BASE_URL


def test_choose_and_ignore_task(memory: Memory, task_key_generator: TaskKeyGeneratorForTest,
                                fvp_session_set: FvpSessionSetForTest, test_dependencies: Dependencies, app: TestApp,
                                fake: TodolistFaker) -> None:

    # given
    bottle_config.dependencies = test_dependencies
    task_1 = fake.a_task()
    task_2 = fake.a_task()
    task_3 = fake.a_task()

    fvp_session_set.feed(
        FvpSnapshot(OrderedDict[TaskKey, TaskKey]({task_2.to_key(): task_1.to_key(), task_1.to_key(): task_3.to_key()})))

    todolist = fake.a_todolist().having(name="todolist", tasks=[task_1, task_2, task_3])
    memory.save(user_key="todo@user.com", todolist=todolist.to_snapshot())

    # when
    response = app.post(f'{BASE_URL}/{todolist.name}/reset')

    # then
    assert fvp_session_set.by() == FvpSnapshot(OrderedDict[TaskKey, TaskKey]({}))
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
