from dataclasses import dataclass
from datetime import date
from uuid import UUID

from expression import Option, Nothing, Some
from peewee import Database, DoesNotExist  # type: ignore

from infra.peewee.table import Task as TaskRow, Todolist as TodolistRow, Session as SessionRow


@dataclass(frozen=True, eq=True)
class Task:
    key: UUID
    name: str
    is_open: bool
    execution_date: Option[date]

    @classmethod
    def from_row(cls, row: TaskRow) -> 'Task':
        return Task(key=row.key, name=row.name, is_open=row.is_open, execution_date=Some(row.execution_date) if row.execution_date else Nothing)


@dataclass(frozen=True, eq=True)
class Todolist:
    name: str

    @classmethod
    def from_row(cls, row: TodolistRow) -> 'Todolist':
        return Todolist(name=row.name)


@dataclass(frozen=True, eq=True)
class FvpSession:
    priorities: list[tuple[UUID, UUID]]



class TodolistDoesNotExist(Exception):
    pass


class PeeweeSdk:
    def __init__(self, database: Database):
        self._database = database

    def all_tasks(self, todolist_name: str) -> list[Task]:
        with self._database.bind_ctx([TaskRow]):
            return [Task.from_row(row) for row in TaskRow.select().where(TaskRow.todolist_name == todolist_name)]

    def task_by(self, todolist_name: str, task_key: UUID) -> Task:
        with self._database.bind_ctx([TaskRow]):
            row = TaskRow.get(TaskRow.todolist_name == todolist_name, TaskRow.key == task_key)
            return Task.from_row(row)

    def all_todolist(self) -> list[Todolist]:
        with self._database.bind_ctx([TodolistRow, TaskRow]):
            query = TodolistRow.select(TodolistRow.name).execute()
            return [Todolist.from_row(row) for row in query]

    def all_open_tasks(self, todolist_name):
        with self._database.bind_ctx([TaskRow]):
            query = TaskRow.select().where(TaskRow.todolist_name == todolist_name, TaskRow.is_open == True)
            return [Task.from_row(row) for row in query]

    def todolist_by(self, todolist_name: str) -> Todolist:
        with self._database.bind_ctx([TodolistRow, TaskRow]):
            try:
                row = TodolistRow.get(TodolistRow.name == todolist_name)
                return Todolist.from_row(row)
            except DoesNotExist:
                raise TodolistDoesNotExist()

    def upsert_todolist(self, todolist: Todolist, tasks: list[Task]):
        with self._database.bind_ctx([TodolistRow, TaskRow]):
            with self._database.atomic() as transaction:
                self._delete_previous_todolist(todolist.name)
                self._save_todolist(todolist, tasks=tasks)

    @staticmethod
    def _save_todolist(todolist: Todolist, tasks: list[Task]):
        TodolistRow.create(name=todolist.name)
        for task in tasks:
            TaskRow.create(todolist_name=todolist.name, key=task.key, name=task.name, is_open=task.is_open, execution_date=task.execution_date.default_value(None))

    @staticmethod
    def _delete_previous_todolist(todolist_name: str) -> None:
        TodolistRow.delete().where(TodolistRow.name == todolist_name).execute()
        TaskRow.delete().where(TaskRow.todolist_name == todolist_name).execute()

    def create_tables(self) -> None:
        created_table = [TodolistRow, TaskRow, SessionRow]
        with self._database.bind_ctx(created_table):
            self._database.create_tables(created_table)

    def upsert_fvp_session(self, fvp_session: FvpSession) -> None:
        with self._database.bind_ctx([SessionRow]):
            with self._database.atomic() as transaction:
                SessionRow.delete().execute()
                for ignored, chosen in fvp_session.priorities:
                    SessionRow.create(ignored=ignored, chosen=chosen)

    def fvp_session_by(self) -> FvpSession:
        with self._database.bind_ctx([SessionRow]):
            return FvpSession(priorities=[(session.ignored, session.chosen) for session in SessionRow.select()])
