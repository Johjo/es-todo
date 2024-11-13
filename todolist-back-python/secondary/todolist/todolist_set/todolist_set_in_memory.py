from expression import Option

from dependencies import Dependencies
from hexagon.shared.type import TodolistName
from hexagon.todolist.aggregate import TodolistSnapshot
from hexagon.todolist.port import TodolistSetPort
from infra.memory import Memory


class TodolistSetInMemory(TodolistSetPort):
    def __init__(self, memory: Memory):
        self.memory = memory

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        return self.memory.by(todolist_name)

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self.memory.save(snapshot)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'TodolistSetInMemory':
        memory = dependencies.get_infrastructure(Memory)
        return TodolistSetInMemory(memory)
