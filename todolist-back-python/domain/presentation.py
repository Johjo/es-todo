from dataclasses import dataclass

from domain.todo.item_status import ItemStatus
from hexagon.fvp.type import TaskKey


@dataclass
class NothingToDo:
    pass


@dataclass
class DoTheTask:
    index: TaskKey
    name: str


@dataclass
class ChooseTheTask:
    index_1: TaskKey
    name_1: str
    index_2: TaskKey
    name_2: str


@dataclass
class ItemPresentation:
    index: TaskKey
    name: str
    done: bool

    @staticmethod
    def build_from(item):
        return ItemPresentation(index=item.index, name=item.name, done=item.status == ItemStatus.CLOSED)
