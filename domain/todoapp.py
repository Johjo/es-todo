from collections import OrderedDict
from dataclasses import dataclass
from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event
from enum import Enum

from domain.presentation import NothingToDo, DoTheTask, ChooseTheTask, ItemPresentation


class ItemStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class FvpStatus(Enum):
    NEXT = "Next"
    LATER = "Later"


@dataclass
class Item:
    index: int
    name: str
    status: ItemStatus
    fvp_status: FvpStatus = FvpStatus.NEXT

    def to_do_the_task(self):
        return DoTheTask(index=self.index, name=self.name)

    def to_choose_the_task(self, other_task):
        return ChooseTheTask(index_1=self.index, name_1=self.name, index_2=other_task.index, name_2=other_task.name)


class TodoList(Aggregate):
    @event("Started")
    def __init__(self, name):
        self.items = OrderedDict()
        self.fvp_index = []

    @event("ItemAdded")
    def add_item(self, item):
        next_id = len(self.items) + 1
        self.items[next_id] = Item(index=next_id, status=ItemStatus.OPEN, name=item)

    def all_items(self):
        return self.items.values()

    @staticmethod
    def create_id(name: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"/todo_list/{name}")

    @event("ItemClosed")
    def close(self, index):
        self.items[index].status = ItemStatus.CLOSED

        if index in self.fvp_index:
            self.fvp_index.remove(index)

        for item in self.items.values():
            if item.index > index:
                item.fvp_status = FvpStatus.NEXT

    def which_task(self):
        last_index = self.fvp_index =self.fvp_index[-1] if self.fvp_index else 0
        items = [item for item in self.items.values() if item.status == ItemStatus.OPEN and item.index >= last_index]

        if items:
            items[0].fvp_status = FvpStatus.NEXT

        items = [item for item in items if item.fvp_status != FvpStatus.LATER]

        if not items:
            return NothingToDo()

        if len(items) == 1:
            return items[0].to_do_the_task()

        return ChooseTheTask(index_1=items[0].index, name_1=items[0].name, index_2=items[1].index, name_2=items[1].name)



    @event("TaskChosen")
    def choose_and_ignore_task(self, chosen_index, ignored_index):
        if chosen_index not in self.fvp_index:
            self.fvp_index.append(chosen_index)
        self.items[ignored_index].fvp_status = FvpStatus.LATER


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
        return [ItemPresentation.build_from(item) for item in todolist.all_items() if item.status == ItemStatus.OPEN]

    @staticmethod
    def open_todolist(name):
        return TodoList.create_id(name)

    def close_item(self, todolist_id, item_index):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.close(index=item_index)
        self.save(todolist)

    def which_task(self, todolist_id):
        todolist: TodoList = self.repository.get(todolist_id)
        return todolist.which_task()

    def choose_and_ignore_task(self, todolist_id, chosen_index, ignored_index):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.choose_and_ignore_task(chosen_index, ignored_index)
        self.save(todolist)

