from dataclasses import dataclass
from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event
from enum import Enum


class ItemStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"


@dataclass
class Item:
    index: int
    name: str
    status: ItemStatus


class TodoList(Aggregate):
    @event("Started")
    def __init__(self, name):
        self.items = []

    @event("ItemAdded")
    def add_item(self, item):
        next_id = len(self.items) + 1
        self.items.append(Item(index=next_id, status=ItemStatus.OPEN, name=item))

    def all_items(self):
        return self.items

    @staticmethod
    def create_id(name: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"/todo_list/{name}")

    @event("ItemClosed")
    def close(self, index):
        self.items[index - 1].status = ItemStatus.CLOSED


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
        return [item for item in todolist.all_items() if item.status == ItemStatus.OPEN]


    @staticmethod
    def open_todolist(name):
        return TodoList.create_id(name)

    def close_item(self, todolist_id, item_index):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.close(index=item_index)
        self.save(todolist)
