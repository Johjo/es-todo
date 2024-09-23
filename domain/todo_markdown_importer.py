import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


class TodoWriter(ABC):
    @abstractmethod
    def write(self, task):
        pass


@dataclass
class Task:
    name: str

class TodoMarkdownImporter:
    def __init__(self, writer: TodoWriter):
        self.writer = writer

    def import_from_markdown(self, markdown):
        pattern = r"- \[ \] (.+)"
        names = re.findall(pattern, markdown)
        for name in names:
            self.writer.write(Task(name))


