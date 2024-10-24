from collections import OrderedDict
from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.shared.type import TaskKey
from primary.web.pages import bottle_config
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.fixture import a_task_key, TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_choose_and_ignore_task(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                                fvp_session_set: FvpSessionSetForTest, test_dependencies: Dependencies, app: TestApp,
                                fake: TodolistFaker):

    bottle_config.dependencies = test_dependencies
    task_1 = replace(fake.a_task_old(1), name="buy the milk")
    task_2 = replace(fake.a_task_old(2), name="buy the water")
    task_3 = replace(fake.a_task_old(3), name="buy the water")

    fvp_session_set.feed(
        FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(1): a_task_key(3)})))

    todolist = replace(fake.a_todolist_old(), name="todolist", tasks=[task_1, task_2, task_3])
    todolist_set.feed(todolist)

    response = app.post(f'/todo/{todolist.name}/reset')
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
    assert fvp_session_set.by() == FvpSnapshot(OrderedDict[TaskKey, TaskKey]({}))
