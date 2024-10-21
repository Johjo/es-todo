import os
from pathlib import Path
from uuid import uuid4

from peewee import Database, SqliteDatabase  # type: ignore

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
from secondary.todolist.table import Todolist as DbTodolist, Task as DbTask
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee as WhichTask_Port_Todolist_Peewee


class TaskKeyGeneratorRandom(OpenTask_Port_TaskKeyGenerator):

    def generate(self) -> TaskKey:
        return TaskKey(uuid4())


def inject_adapter(dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(Todolist_Port_TodolistSet, TodolistSetPeewee.factory)

    task_key_generator = TaskKeyGeneratorRandom()
    dependencies = dependencies.feed_adapter(OpenTask_Port_TaskKeyGenerator, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(WhichTask_Port_Todolist, WhichTask_Port_Todolist_Peewee.factory)
    dependencies = dependencies.feed_adapter(FinalVersionPerfected_Port_SessionSet, JsonSessionRepository.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetPeewee.factory)

    return dependencies


def inject_path(dependencies: Dependencies) -> Dependencies:
    dependencies = dependencies.feed_path("todolist_json_path", lambda _: Path("./test_todolist.json"))
    dependencies = dependencies.feed_path("session_fvp_json_path", lambda _: Path("./test_fvp.json"))
    return dependencies


def inject_infrastructure(dependencies: Dependencies) -> Dependencies:
    database = SqliteDatabase("todolist.db.sqlite")
    with database.bind_ctx([DbTodolist, DbTask]):
        database.create_tables([DbTodolist, DbTask])
    dependencies =  dependencies.feed_infrastructure(Database, lambda _: database)
    return dependencies


def start():
    from dotenv import load_dotenv
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = inject_adapter(dependencies=dependencies)
    dependencies = inject_path(dependencies=dependencies)
    dependencies = inject_infrastructure(dependencies=dependencies)
    bottle_config.dependencies = dependencies
    load_dotenv()
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    bottle_app.run(reloader=True, host=host, port=port, debug=True)


if __name__ == '__main__':
    start()
