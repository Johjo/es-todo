
from expression import Option

from src.dependencies import Dependencies
from src.hexagon.shared.type import TodolistName
from src.hexagon.todolist.aggregate import TodolistSnapshot
from src.hexagon.todolist.port import TodolistSetPort
from src.infra.memory import Memory
from src.shared.const import USER_KEY


class TodolistSetInMemory(TodolistSetPort):
    def __init__(self, memory: Memory, user_key: str):
        self.memory = memory
        self._user_key = user_key

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        return self.memory.by(user_key=self._user_key, todolist_name=todolist_name)

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self.memory.save(user_key=self._user_key, todolist=todolist)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetInMemory':
        return TodolistSetInMemory(
            memory=dependencies.get_infrastructure(Memory),
            user_key=dependencies.get_data(USER_KEY))
