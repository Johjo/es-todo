from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Task:
    id: UUID
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }

@dataclass
class TodoList:
    tasks: list[Task]
    number_of_tasks: int
    contexts: list[str]

    def __post_init__(self):
        assert len(self.tasks) <= 2, "Todolist can only have 2 tasks to examine at most"

    def to_dict(self):
        return {
            "tasks": [task.to_dict() for task in self.tasks],
            "number_of_tasks": self.number_of_tasks,
            "contexts": self.contexts
        }


def todolist(name) -> TodoList:
    return TodoList(tasks=[
        Task(id=uuid4(), name="todo 1 #context1"),
        Task(id=uuid4(), name="todo 2 #context2")],
        number_of_tasks=2,
        contexts=["#context1", "#context2"])
