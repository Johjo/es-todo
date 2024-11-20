import os
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from peewee import Database, SqliteDatabase  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.shared.type import TaskKey
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from infra.peewee.sdk import PeeweeSdk
from primary.controller.dependencies import inject_use_cases
from primary.controller.read.final_version_perfected import CalendarPort
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config, bottle_app
from secondary.fvp.read.which_task.todolist_peewee import TodolistPeewee
from secondary.todolist.todolist_set_peewee import TodolistSetPeewee, TodolistSetReadPeewee


class TaskKeyGeneratorRandom(TaskKeyGeneratorPort):

    def generate(self) -> TaskKey:
        return TaskKey(uuid4())


def inject_final_version_perfected(dependencies: Dependencies) -> Dependencies:
    from secondary.fvp.write.session_set_peewee import SessionPeewee
    from hexagon.fvp.aggregate import FvpSessionSetPort

    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionPeewee.factory)
    return dependencies


class Calendar(CalendarPort):
    def today(self) -> date:
        return datetime.today().date()

    @classmethod
    def factory(cls, _: Dependencies) -> 'Calendar':
        return Calendar()


def inject_adapter(dependencies: Dependencies):
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetPeewee.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadPeewee.factory)
    dependencies = inject_final_version_perfected(dependencies)

    task_key_generator = TaskKeyGeneratorRandom()
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistPeewee.factory)
    dependencies = dependencies.feed_adapter(CalendarPort, Calendar.factory)

    return dependencies


def inject_infrastructure(dependencies: Dependencies) -> Dependencies:
    path = dependencies.get_path("sqlite_database_path")
    database = SqliteDatabase(path)
    sdk = PeeweeSdk(database)
    sdk.create_tables()
    dependencies = dependencies.feed_infrastructure(Database, lambda _: database)
    return dependencies


def inject_all_dependencies(dependencies: Dependencies):
    dependencies = inject_use_cases(dependencies)
    dependencies = inject_adapter(dependencies)
    dependencies = inject_infrastructure(dependencies)
    from dotenv import load_dotenv
    load_dotenv()
    static_path = os.environ["STATIC_PATH"]
    dependencies = dependencies.feed_path("static_path", lambda _: Path(static_path))

    return dependencies


def start():
    from dotenv import load_dotenv
    dependencies = bottle_config.dependencies
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: Path("./todolist.db.sqlite"))
    dependencies = inject_all_dependencies(dependencies)
    bottle_config.dependencies = dependencies
    load_dotenv()
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    bottle_app.run(reloader=True, host=host, port=port, debug=True)


if __name__ == '__main__':
    start()
