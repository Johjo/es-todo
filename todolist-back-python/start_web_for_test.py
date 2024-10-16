import os
from pathlib import Path

from hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from hexagon.fvp.read.which_task import TodolistPort as WhichTask_Port_Todolist
from hexagon.todolist.port import TodolistSetPort as Todolist_Port_TodolistSet, \
    TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from hexagon.todolist.aggregate import TaskKey

from primary.controller.dependencies import inject_use_cases
from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config, bottle_app
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from secondary.todolist.todolist_set_json import TodolistSetJson
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.primary.web.conftest import TodolistForTest


class TaskKeyGeneratorIncremental(OpenTask_Port_TaskKeyGenerator):
    def __init__(self):
        self.current = 0

    def generate(self) -> TaskKey:
        self.current += 1
        return TaskKey(self.current)


def inject_adapter(dependencies: Dependencies):
    todolist_set = TodolistSetForTest()
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, TodolistSetJson.factory)

    task_key_generator = TaskKeyGeneratorIncremental()
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)

    which_task_todolist = TodolistForTest(todolist_set)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, lambda _: which_task_todolist)

    fvp_session_set = FvpSessionSetForTest()
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, lambda _: fvp_session_set)

    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadJson.factory)

    return dependencies


def inject_path(dependencies: Dependencies) -> Dependencies:
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: Path("test_todolist.json"))
    return dependencies


def start():
    from dotenv import load_dotenv
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = inject_adapter(dependencies=dependencies)
    dependencies = inject_path(dependencies=dependencies)
    bottle_config.dependencies = dependencies
    load_dotenv()
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    bottle_app.run(reloader=True, host=host, port=port, debug=True)


if __name__ == '__main__':
    start()
