import re
from abc import ABC, abstractmethod
from collections import defaultdict


class OpenTaskReader(ABC):
    @abstractmethod
    def all(self) -> list[str]:
        pass


class TodoContextQuery:
    def __init__(self, set_of_open_tasks: OpenTaskReader):
        self.set_of_open_tasks = set_of_open_tasks

    def all_contexts(self):
        context_count = defaultdict(int)
        for task in self.set_of_open_tasks.all():
            for context in self.context_from(task):
                context_count[context] += 1
        return context_count

    @staticmethod
    def context_from(task):
        pattern = r"[#@][a-zA-Z0-9_-]+"
        all_contexts = re.findall(pattern, task)
        return set([context.lower() for context in all_contexts])
