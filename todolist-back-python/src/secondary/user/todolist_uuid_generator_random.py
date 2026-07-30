from uuid import uuid4

from hexagon.shared.type import TodolistKey
from hexagon.user.port import TodolistUuidGeneratorPort


class TodolistUuidGeneratorRandom(TodolistUuidGeneratorPort):
    def generate_todolist_key(self) -> TodolistKey:
        return TodolistKey(uuid4())
