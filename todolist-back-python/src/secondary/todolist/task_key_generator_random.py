from uuid import uuid4

from src.hexagon.shared.type import TaskKey
from src.hexagon.todolist.port import TaskKeyGeneratorPort


class TaskKeyGeneratorRandom(TaskKeyGeneratorPort):
    def generate(self) -> TaskKey:
        return TaskKey(uuid4())
