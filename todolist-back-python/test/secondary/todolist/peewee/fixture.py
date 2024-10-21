from peewee import Database

from hexagon.todolist.aggregate import TodolistSnapshot
from secondary.todolist.table import Task, Todolist


def feed_todolist(todolist: TodolistSnapshot, database: Database) -> None:
    with database.bind_ctx([Todolist, Task]):
        Todolist.create(name=todolist.name)
        for task in todolist.tasks:
            Task.create(todolist_name=todolist.name, key=task.key, name=task.name, is_open=task.is_open)
