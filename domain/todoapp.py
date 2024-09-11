from dataclasses import dataclass
from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event

@dataclass
class Item:
    name: str

class TodoList(Aggregate):
    @event("Started")
    def __init__(self, name):
        self.items = []

    @event("ItemAdded")
    def add_item(self, item):
        self.items.append(Item(item))

    def all_items(self):
        return self.items

    @staticmethod
    def create_id(name: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"/todo_list/{name}")


class TodoApp(Application):
    def start_todolist(self, name):
        todolist = TodoList(name)
        self.save(todolist)
        return todolist.id

    def add_item(self, todolist_id, item):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.add_item(item)
        self.save(todolist)

    def get_open_items(self, todolist_id):
        todolist: TodoList = self.repository.get(todolist_id)
        return todolist.all_items()

    @staticmethod
    def open_todolist(name):
        return TodoList.create_id(name)
