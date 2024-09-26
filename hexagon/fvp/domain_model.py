from collections import OrderedDict
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Task:
    id: uuid4
    name: str

    def to_do_the_task(self):
        return DoTheTask(id=self.id, name=self.name)

    def to_choose_the_task(self, other_task):
        return ChooseTheTask(id_1=self.id, name_1=self.name, id_2=other_task.id, name_2=other_task.name)


@dataclass
class NothingToDo:
    pass


@dataclass
class DoTheTask:
    id: uuid4
    name: str


@dataclass
class ChooseTheTask:
    id_1: uuid4
    name_1: str
    id_2: uuid4
    name_2: str


class FinalVersionPerfected:
    def __init__(self):
        self.priority_of_task = OrderedDict()

    def which_task(self, open_tasks: list[Task]):
        if not open_tasks:
            return NothingToDo()

        tasks_to_priorize = self._all_tasks_to_priorize(open_tasks)

        if len(tasks_to_priorize) == 1:
            return tasks_to_priorize[0].to_do_the_task()

        return tasks_to_priorize[0].to_choose_the_task(tasks_to_priorize[1])

    def _all_tasks_to_priorize(self, open_tasks):
        max_priority = max([self.priority_of_task.get(task.id, 0) for task in open_tasks])
        tasks_to_priorize = [task for task in open_tasks if
                             self.priority_of_task.get(task.id, max_priority) == max_priority]
        return tasks_to_priorize

    def choose_and_ignore_task(self, id_chosen, id_ignored):
        if id_chosen not in self.priority_of_task:
            self.priority_of_task[id_chosen] = self.priority_of_task.get(id_ignored, 0) + 1

        self.priority_of_task[id_ignored] = self.priority_of_task[id_chosen] - 1
