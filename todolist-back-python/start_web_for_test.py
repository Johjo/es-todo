import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from dependencies import Dependencies
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.shared.type import TaskKey
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from primary.controller.dependencies import inject_use_cases
from primary.controller.read.final_version_perfected import CalendarPort
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config, bottle_app
from secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite
from secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite
from secondary.todolist.todolist_set_read.todolist_set_read_sqlite import TodolistSetReadSqlite


class TaskKeyGeneratorRandom(TaskKeyGeneratorPort):

    def generate(self) -> TaskKey:
        return TaskKey(uuid4())


def inject_final_version_perfected(dependencies: Dependencies) -> Dependencies:
    from secondary.fvp.write.session_set_sqlite import SessionSqlite
    from hexagon.fvp.aggregate import FvpSessionSetPort

    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionSqlite.factory)
    return dependencies


class Calendar(CalendarPort):
    def today(self) -> date:
        return datetime.today().date()

    @classmethod
    def factory(cls, _: Dependencies) -> 'Calendar':
        return Calendar()


def inject_adapter(dependencies: Dependencies) -> Dependencies:
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetSqlite.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadSqlite.factory)
    dependencies = inject_final_version_perfected(dependencies)

    task_key_generator = TaskKeyGeneratorRandom()
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistSqlite.factory)
    dependencies = dependencies.feed_adapter(CalendarPort, Calendar.factory)

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
    from dotenv import load_dotenv
    load_dotenv()
    static_path = os.environ["STATIC_PATH"]
    dependencies = dependencies.feed_path("static_path", lambda _: Path(static_path))

    return dependencies


def start() -> None:
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
