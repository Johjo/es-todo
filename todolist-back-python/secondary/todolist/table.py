from enum import unique

from peewee import CharField, UUIDField, BooleanField, DatabaseProxy, Model  # type: ignore


class Task(Model):
    todolist_name = CharField()
    key = UUIDField(primary_key=True)
    name = CharField()
    is_open = BooleanField()


class Todolist(Model):
    name = CharField(primary_key=True)
