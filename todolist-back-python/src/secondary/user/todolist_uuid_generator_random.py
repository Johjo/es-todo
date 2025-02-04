from uuid import uuid4

from src.hexagon.shared.type import TodolistKey
from src.hexagon.user.port import TodolistUuidGeneratorPort


class TodolistUuidGeneratorRandom(TodolistUuidGeneratorPort):
    def generate_todolist_key(self) -> TodolistKey:
        return TodolistKey(uuid4())
