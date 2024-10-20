from peewee import CharField, UUIDField, BooleanField, DatabaseProxy, Model  # type: ignore

database_proxy = DatabaseProxy()  # Create a proxy for our db.

class BaseModel(Model):
    class Meta:
        database = database_proxy


class Task(BaseModel):
    todolist_name = CharField()
    key = UUIDField()
    name = CharField()
    is_open = BooleanField()




class Todolist(BaseModel):
    name = CharField()
