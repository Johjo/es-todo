from abc import ABC, abstractmethod
from dataclasses import dataclass


class TodoReader(ABC):
    @abstractmethod
    def all_tasks(self):
        pass


class TodoMarkdownExporter:
    def __init__(self, reader: TodoReader):
        self.reader = reader

    def export_to_markdown(self) -> str:
        lines = [task.to_markdown() for task in self.reader.all_tasks()]
        return "\n".join(lines)


@dataclass
class Task:
    name: str
    done: bool

    def to_markdown(self):
        state = "- [x] " if self.done else "- [ ] "
        return state + self.name
