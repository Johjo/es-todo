import re

from expression import Option, Nothing, Some
from peewee import DoesNotExist

from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount, TaskKey
from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from hexagon.todolist.port import TodolistSetPort
from primary.controller.read.todolist import TodolistSetReadPort, Task
from secondary.todolist.table import Task as DbTask, Todolist as DbTodolist


class TodolistSetPeewee(TodolistSetPort, TodolistSetReadPort):

    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        raise NotImplementedError()

    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        task = DbTask.get(DbTask.todolist_name == todolist_name, DbTask.key == task_key)
        return Task(id=task.key, name=task.name, is_open=task.is_open)

    def all_by_name(self) -> list[TodolistName]:
        query = DbTodolist.select(DbTodolist.name).execute()
        return [TodolistName(todolist.name) for todolist in query]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        tasks = DbTask.select(DbTask.name).where(DbTask.todolist_name == todolist_name)
        counts_by_context = {}
        for task in tasks:
            contexts = self._extract_context_from_name(task)
            for context in contexts:
                counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(context, count) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        print(task.name, contexts)
        return [TodolistContext(context.lower()) for context in contexts]

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        try:
            todolist = DbTodolist.get(DbTodolist.name == todolist_name)
        except DoesNotExist:
            return Nothing
        tasks = DbTask.select().where(DbTask.todolist_name == todolist_name)
        return Some(self._to_todolist_snapshot(todolist, tasks))

    def _to_todolist_snapshot(self, todolist, tasks):
        return TodolistSnapshot(name=todolist.name, tasks=[self._to_task_snapshot(task) for task in tasks])

    @staticmethod
    def _to_task_snapshot(task):
        return TaskSnapshot(key=task.key, name=task.name, is_open=task.is_open)

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self.delete_previous_tasks(snapshot)
        self.save_todolist(snapshot)

    @staticmethod
    def save_todolist(snapshot):
        DbTodolist.create(name=snapshot.name)
        for task in snapshot.tasks:
            DbTask.create(todolist_name=snapshot.name, key=task.key, name=task.name, is_open=task.is_open)

    @staticmethod
    def delete_previous_tasks(snapshot):
        DbTask.delete().where(DbTask.todolist_name == snapshot.name).execute()

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetPeewee':
        return TodolistSetPeewee()


