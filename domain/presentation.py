from dataclasses import dataclass

from domain.todo.item_status import ItemStatus


@dataclass
class NothingToDo:
    pass


@dataclass
class DoTheTask:
    index: int
    name: str


@dataclass
class ChooseTheTask:
    index_1: int
    name_1: str
    index_2: int
    name_2: str


@dataclass
class ItemPresentation:
    index: int
    name: str
    done: bool

    @staticmethod
    def build_from(item):
        return ItemPresentation(index=item.index, name=item.name, done=item.status == ItemStatus.CLOSED)
