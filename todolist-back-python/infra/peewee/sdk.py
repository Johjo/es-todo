from datetime import datetime
from typing import Any
from uuid import UUID

from expression import Nothing, Some
from peewee import Database, DoesNotExist  # type: ignore

from infra.peewee.type import Task, Todolist, FvpSession, TodolistDoesNotExist
from test.hexagon.fvp.read.test_which_task import todolist_name


class SqliteSdk:
    def __init__(self, database: Database):
        self._database = database

    def all_tasks(self, user_key: str, todolist_name: str) -> list[Task]:
        cursor = self._database.cursor()
        todolist_id : int
        cursor.execute(
            "SELECT key, Task.name as name, is_open, execution_date from Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE todolist.user_key = ? and todolist.name = ?",
            (user_key, todolist_name,))
        return [self.to_task(row) for row in cursor.fetchall()]

    @staticmethod
    def to_task(row: Any) -> Task:
        execution_date = row[3]
        task = Task(key=UUID(row[0]),
                    name=row[1],
                    is_open=row[2] == 1,
                    execution_date=Some(datetime.strptime(execution_date, "%Y-%m-%d").date()) if execution_date is not None else Nothing)
        return task

    def task_by(self, todolist_name: str, task_key: UUID) -> Task:
        cursor = self._database.cursor()
        cursor.execute("SELECT key, Task.name as name, is_open, execution_date FROM Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE todolist.name = ? and key = ?", (todolist_name, str(task_key)))
        fetchone = cursor.fetchone()
        return self.to_task(fetchone)

    def all_todolist(self) -> list[Todolist]:
        cursor = self._database.cursor()
        cursor.execute("SELECT name from Todolist ORDER BY name")
        return [Todolist.from_row(row) for row in cursor.fetchall()]

    def all_open_tasks(self, user_key: str, todolist_name: str):
        cursor = self._database.cursor()
        cursor.execute("SELECT key, Task.name as name, is_open, execution_date FROM Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE Todolist.name = ? and is_open = ?", (todolist_name, True))
        return [self.to_task(row) for row in cursor.fetchall()]

    def todolist_by(self, user_key: str, todolist_name: str) -> Todolist:
        cursor = self._database.cursor()
        cursor.execute("SELECT name from Todolist where name = ? and user_key = ?", (todolist_name, user_key))
        row = cursor.fetchone()
        if not row:
            raise TodolistDoesNotExist()
        return Todolist.from_row(row)

    def upsert_todolist(self, user_key: str, todolist: Todolist, tasks: list[Task]):
        self._delete_previous_todolist(user_key=user_key, todolist_name=todolist.name)
        self._save_todolist(user_key=user_key, todolist_name=todolist.name, tasks=tasks)

    def _save_todolist(self, user_key: str, todolist_name: str, tasks: list[Task]):
        cursor = self._database.cursor()
        cursor.execute("INSERT into Todolist (user_key, name) VALUES (?, ?) ", (user_key, todolist_name,))
        todolist_id = self._todolist_id(user_key, todolist_name)
        for task in tasks:
            cursor.execute("INSERT into TASK (todolist_id, key, name, is_open, execution_date) VALUES (?, ?, ?, ?, ?)",
                           (todolist_id, str(task.key), task.name, task.is_open, task.execution_date.default_value(None)))

    def _todolist_id(self, user_key: str, todolist_name: str) -> int:
        cursor = self._database.cursor()
        cursor.execute("SELECT id from Todolist where user_key=? and name=?", (user_key, todolist_name))
        todolist_id: int = cursor.fetchone()[0]
        return todolist_id

    def _delete_previous_todolist(self, user_key: str, todolist_name: str) -> None:
        cursor = self._database.cursor()
        cursor.execute("SELECT id from Todolist where user_key=? and name=?", (user_key, todolist_name))
        row = cursor.fetchone()
        if row:
            todolist_id : int = row[0]
            cursor.execute("DELETE from Todolist where id = ?", (todolist_id, ))
            cursor.execute("DELETE from Task where todolist_id = ?", (todolist_id, ))


    def create_tables(self) -> None:
        cursor = self._database.cursor()
        cursor.execute("CREATE TABLE Todolist(id INTEGER PRIMARY KEY AUTOINCREMENT, name, user_key)")
        cursor.execute("CREATE INDEX todolist_name_idx ON Todolist (name);")

        cursor.execute("CREATE TABLE Task(id INTEGER PRIMARY KEY AUTOINCREMENT, todolist_id, key, name, is_open, execution_date)")

        cursor.execute("CREATE TABLE Session(id INTEGER PRIMARY KEY AUTOINCREMENT, ignored_task_key, chosen_task_key)")


    def upsert_fvp_session(self, fvp_session: FvpSession) -> None:
        cursor = self._database.cursor()
        cursor.execute("DELETE FROM Session")
        for ignored, chosen in fvp_session.priorities:
            cursor.execute("INSERT INTO Session(ignored_task_key, chosen_task_key) VALUES (?, ?)", (str(ignored), str(chosen)))

    def fvp_session_by(self) -> FvpSession:
        cursor = self._database.cursor()
        cursor.execute("SELECT ignored_task_key, chosen_task_key FROM Session")
        rows = cursor.fetchall()
        return FvpSession(priorities=[(UUID(session[0]), UUID(session[1])) for session in rows])
