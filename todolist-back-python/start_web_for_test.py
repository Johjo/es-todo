import os
from pathlib import Path
from uuid import uuid4

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort as FinalVersionPerfected_Port_SessionSet
from hexagon.fvp.read.which_task import TodolistPort as WhichTask_Port_Todolist
from hexagon.shared.type import TaskKey
from hexagon.todolist.port import TodolistSetPort as Todolist_Port_TodolistSet, \
    TaskKeyGeneratorPort as OpenTask_Port_TaskKeyGenerator
from primary.controller.dependencies import inject_use_cases
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config, bottle_app
from secondary.fvp.json_session_repository import JsonSessionRepository
from secondary.todolist.todolist_set_json import TodolistSetJson
from secondary.todolist.todolist_set_read_json import TodolistSetReadJson
from test.secondary.fvp.read.which_task.test_todolist_json import TodolistJson as WhichTask_Port_Todolist_Json


class TaskKeyGeneratorRandom(OpenTask_Port_TaskKeyGenerator):

    def generate(self) -> TaskKey:
        return TaskKey(uuid4())


def inject_adapter(dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, TodolistSetJson.factory)

    task_key_generator = TaskKeyGeneratorRandom()
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, WhichTask_Port_Todolist_Json.factory)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, JsonSessionRepository.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadJson.factory)

    return dependencies


def inject_path(dependencies: Dependencies) -> Dependencies:
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: Path("./test_todolist.json"))
    dependencies = dependencies.feed_path("session_fvp_json_path", lambda _: Path("./test_fvp.json"))
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
