from collections import OrderedDict

from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.shared.type import TaskKey, UserKey
from src.infra.fvp_memory import FvpMemory
from src.infra.memory import Memory
from src.primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse, BASE_URL, header_with_good_authentication


def test_choose_and_ignore_task(memory: Memory, task_key_generator: TaskKeyGeneratorForTest,
                                fvp_memory: FvpMemory, dependencies: Dependencies, app: TestApp,
                                fake: TodolistFaker) -> None:

    # GIVEN
    bottle_config.dependencies = dependencies
    task_1 = fake.a_task(1).having(name="buy the milk")
    task_2 = fake.a_task(2).having(name="buy the water")
    task_3 = fake.a_task(3).having(name="buy the water")

    fvp_memory.feed(user_key=UserKey("test@mail.fr"),snapshot=
        FvpSnapshot(OrderedDict[TaskKey, TaskKey]({
            task_2.to_key(): task_1.to_key(),
            task_1.to_key(): task_3.to_key()})))

    todolist = fake.a_todolist().having(tasks=[task_1, task_2, task_3])
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())

    # WHEN
    response = app.post(f'{BASE_URL}/{todolist.name}/item/{task_3.to_key()}/cancel_priority', headers=header_with_good_authentication())

    # THEN
    assert fvp_memory.by(user_key=UserKey("test@mail.fr")) == FvpSnapshot(OrderedDict[TaskKey, TaskKey]({task_2.to_key(): task_1.to_key()}))
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
