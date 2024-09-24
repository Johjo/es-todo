from collections import OrderedDict
from dataclasses import dataclass
from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.application import Application
from eventsourcing.domain import Aggregate, event
from enum import Enum

from eventsourcing.utils import register_topic

from domain.presentation import NothingToDo, DoTheTask, ChooseTheTask, ItemPresentation
from domain.todo.item_status import ItemStatus




class FvpStatus(Enum):
    NEXT = "Next"
    LATER = "Later"
    TO_PRIORIZE = "To prioritize"


@dataclass
class Item:
    index: int
    name: str
    status: ItemStatus = ItemStatus.OPEN
    fvp: FvpStatus = FvpStatus.TO_PRIORIZE

    def to_do_the_task(self):
        return DoTheTask(index=self.index, name=self.name)

    def to_choose_the_task(self, other_task):
        return ChooseTheTask(index_1=self.index, name_1=self.name, index_2=other_task.index, name_2=other_task.name)


class TodoList(Aggregate):
    @event("Started")
    def __init__(self, name):
        self.next_index = 0
        self.items = OrderedDict()

    @event("ItemAdded")
    def add_item(self, item):
        self.next_index += 1
        self.items[self.next_index] = Item(index=self.next_index, name=item)
        self._mark_first_open_item_to_next()

    def _mark_first_open_item_to_next(self):
        open_items = [item for item in self.items.values() if item.status == ItemStatus.OPEN]
        if open_items:
            open_items[0].fvp = FvpStatus.NEXT

    def all_items(self):
        return [item for item in self.items.values()]

    @staticmethod
    def create_id(name: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"/todo_list/{name}")

    @event("ItemClosed")
    def close(self, index):
        self.items[index].status = ItemStatus.CLOSED
        open_items = [item for item in self.items.values() if item.status == ItemStatus.OPEN]
        for item in open_items:
            if item.index > index:
                item.fvp = FvpStatus.TO_PRIORIZE
        self._mark_first_open_item_to_next()

    def which_task(self):
        current_item = self.search_last_next_item()
        if not current_item:
            return NothingToDo()

        item_to_priorize = self.search_first_item_to_priorize()
        if not item_to_priorize:
            return current_item.to_do_the_task()

        if item_to_priorize:
            return current_item.to_choose_the_task(item_to_priorize)


    def search_last_next_item(self):
        open_items = [item for item in self.items.values() if item.status == ItemStatus.OPEN and item.fvp == FvpStatus.NEXT]
        if not open_items:
            return None
        return open_items[-1]

    def search_first_item_to_priorize(self):
        open_items = [item for item in self.items.values() if item.status == ItemStatus.OPEN and item.fvp == FvpStatus.TO_PRIORIZE]

        if not open_items:
            return None

        return open_items[0]


    @event("TaskChosen")
    def choose_and_ignore_task(self, chosen_index, ignored_index):
        self.items[chosen_index].fvp = FvpStatus.NEXT
        if self.items[ignored_index].fvp != FvpStatus.NEXT:
            self.items[ignored_index].fvp = FvpStatus.LATER

    @event("FvpReset")
    def reset_fvp_algorithm(self):
        open_items = [item for item in self.items.values() if item.status == ItemStatus.OPEN]
        for item in open_items:
            item.fvp = FvpStatus.TO_PRIORIZE
        self._mark_first_open_item_to_next()

    def all_tasks(self):
        return [ItemPresentation.build_from(item) for item in self.all_items()]

    @event("ItemReworded")
    def reword_item(self, item_id, new_name):
        self.items[item_id].name = new_name

    def get_task(self, task_id):
        return ItemPresentation.build_from(self.items[task_id])


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

    def reset_fvp_algorithm(self, todolist_id):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.reset_fvp_algorithm()
        self.save(todolist)

    def all_tasks(self, todolist_id):
        todolist: TodoList = self.repository.get(todolist_id)
        return todolist.all_tasks()

    def reword_item(self, todolist_id, item_id, new_name):
        todolist: TodoList = self.repository.get(todolist_id)
        todolist.reword_item(item_id, new_name)
        self.save(todolist)

    def get_task(self, todolist_id, task_id):
        todolist: TodoList = self.repository.get(todolist_id)
        return todolist.get_task(task_id)


register_topic("domain.todoapp:TodoList", TodoList)