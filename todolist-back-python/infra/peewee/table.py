from peewee import CharField, UUIDField, BooleanField, Model, DateField  # type: ignore


class Task(Model):
    key = UUIDField(index=True, unique=True)
    todolist_name = CharField(index=True)
    name = CharField()
    is_open = BooleanField()
    execution_date = DateField(null=True)


class Todolist(Model):
    user_key = CharField(index=True)
    name = CharField(index=True)


class Session(Model):
    ignored = UUIDField()
    chosen = UUIDField()



# créer une db v1 + migrer en v2 == créer une db v2
# SELECT name FROM sqlite_master WHERE type='table'
# PRAGMA table_info(%1);