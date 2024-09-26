from abc import ABC, abstractmethod

from hexagon.fvp.domain_model import Task, FinalVersionPerfected


class TaskReader(ABC):
    @abstractmethod
    def all(self) -> list[Task]:
        pass


class WhichTaskQuery:
    def __init__(self, set_of_open_tasks: TaskReader):
        self.set_of_open_tasks = set_of_open_tasks

    def which_task(self):
        fvp = FinalVersionPerfected()
        return fvp.which_task(self.set_of_open_tasks.all())
