import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSessionSetPort
from src.hexagon.fvp.read.which_task import TodolistPort
from src.hexagon.shared.type import TaskKey
from src.hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from src.primary.controller.dependencies import inject_use_cases
from src.primary.controller.read.final_version_perfected import CalendarPort
from src.primary.controller.read.todolist import TodolistSetReadPort
from src.primary.controller.write.todolist import DateTimeProviderPort
from src.primary.web.pages import bottle_config, bottle_app
from src.secondary.datetime_provider import DateTimeProvider
from src.secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite
from src.secondary.fvp.write.session_set_sqlite import SessionSqlite
from src.secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite
from src.secondary.todolist.todolist_set_read.todolist_set_read_sqlite import TodolistSetReadSqlite


class TaskKeyGeneratorRandom(TaskKeyGeneratorPort):
    def generate(self) -> TaskKey:
        return TaskKey(uuid4())


class Calendar(CalendarPort):
    def today(self) -> date:
        return datetime.today().date()

    @classmethod
    def factory(cls, _: Dependencies) -> 'Calendar':
        return Calendar()


def inject_adapter(dependencies: Dependencies) -> Dependencies:
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetSqlite.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadSqlite.factory)
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionSqlite.factory)
    task_key_generator = TaskKeyGeneratorRandom()

    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistSqlite.factory)
    dependencies = dependencies.feed_adapter(CalendarPort, Calendar.factory)
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, DateTimeProvider.factory)

    return dependencies


def inject_infrastructure(dependencies: Dependencies) -> Dependencies:
    path = dependencies.get_path("sqlite_database_path")
    database = sqlite3.connect(path, isolation_level=None)
    dependencies = dependencies.feed_infrastructure(sqlite3.Connection, lambda _: database)
    return dependencies


def inject_all_dependencies(dependencies: Dependencies) -> Dependencies:
    dependencies = inject_use_cases(dependencies)
    dependencies = inject_adapter(dependencies)
    dependencies = inject_infrastructure(dependencies)
    dependencies = inject_environment_variable(dependencies)

    return dependencies


def inject_environment_variable(dependencies):
    load_dotenv()
    dependencies = dependencies.feed_path("static_path", lambda _: Path(os.environ["STATIC_PATH"]))
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: Path(os.environ["DATABASE_PATH"]))
    return dependencies


def start() -> None:
    load_dotenv()
    print(os.environ["HELLO"])
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    database_path = os.environ["DATABASE_PATH"]
    dependencies = bottle_config.dependencies
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: Path(database_path))
    dependencies = inject_all_dependencies(dependencies)
    bottle_config.dependencies = dependencies
    bottle_app.run(reloader=True, host=host, port=port, debug=True)

if __name__ == '__main__':
    start()
