from peewee import CharField, UUIDField, BooleanField, DatabaseProxy, Model, DateField  # type: ignore


class Task(Model):
    todolist_name = CharField(index=True)
    key = UUIDField(primary_key=True)
    name = CharField()
    is_open = BooleanField()
    execution_date = DateField(null=True)


class Todolist(Model):
    name = CharField(primary_key=True)


class Session(Model):
    ignored = UUIDField()
    chosen = UUIDField()



# créer une db v1 + migrer en v2 == créer une db v2
# SELECT name FROM sqlite_master WHERE type='table'
# PRAGMA table_info(%1);