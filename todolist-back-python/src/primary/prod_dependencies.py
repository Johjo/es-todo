import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from primary.controller.read.final_version_perfected import CalendarPort
from primary.controller.read.todolist import TodolistSetReadPort
from primary.controller.use_case_dependencies import inject_use_cases
from primary.controller.write.todolist import DateTimeProviderPort
from secondary.calendar import Calendar
from secondary.datetime_provider import DateTimeProvider
from secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite
from secondary.fvp.write.session_set_sqlite import SessionSqlite
from secondary.todolist.task_key_generator_random import TaskKeyGeneratorRandom
from secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite
from secondary.todolist.todolist_set_read.todolist_set_read_sqlite import TodolistSetReadSqlite


def inject_all_dependencies(dependencies: Dependencies) -> Dependencies:
    dependencies = inject_use_cases(dependencies)
    dependencies = inject_adapter(dependencies)
    dependencies = inject_infrastructure(dependencies)
    dependencies = inject_environment_variable(dependencies)

    return dependencies


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


def inject_environment_variable(dependencies : Dependencies) -> Dependencies:
    load_dotenv()
    dependencies = dependencies.feed_path("static_path", lambda _: Path(os.environ["STATIC_PATH"]))
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: Path(os.environ["DATABASE_PATH"]))
    return dependencies
