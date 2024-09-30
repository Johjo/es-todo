from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class Task:
    id: int
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
    id: int
    name: str


@dataclass
class ChooseTheTask:
    id_1: int
    name_1: str
    id_2: int
    name_2: str


@dataclass(frozen=True)
class FvpSnapshot:
    task_priorities: OrderedDict[int, int]

    def to_primitive_dict(self) -> dict[int, int]:
        return {key: value for key, value in self.task_priorities.items()}

    @classmethod
    def from_primitive_dict(cls, data: dict[int, int]) -> 'FvpSnapshot':
        return FvpSnapshot(OrderedDict[int, int](data))



class FinalVersionPerfectedSession:
    def __init__(self, task_priorities : OrderedDict[int, int]):
        self.task_priorities : OrderedDict[int, int] = task_priorities

    def which_task(self, open_tasks: list[Task]):
        if not open_tasks:
            return NothingToDo()

        tasks_to_priorize = self._all_tasks_to_priorize(open_tasks)

        if len(tasks_to_priorize) == 1:
            return tasks_to_priorize[0].to_do_the_task()

        return tasks_to_priorize[0].to_choose_the_task(tasks_to_priorize[1])

    def _all_tasks_to_priorize(self, open_tasks : list[Task]) -> list[Task]:
        max_priority = max([self.task_priorities.get(task.id, 0) for task in open_tasks])
        tasks_to_priorize = [task for task in open_tasks if
                             self.task_priorities.get(task.id, max_priority) == max_priority]
        return tasks_to_priorize

    def choose_and_ignore_task(self, id_chosen, id_ignored) -> None:
        if id_chosen not in self.task_priorities:
            self.task_priorities[id_chosen] = self.task_priorities.get(id_ignored, 0) + 1

        self.task_priorities[id_ignored] = self.task_priorities[id_chosen] - 1

    def reset(self) -> None:
        self.task_priorities = OrderedDict()

    def to_snapshot(self) -> FvpSnapshot:
        return FvpSnapshot(self.task_priorities)

    @classmethod
    def from_snapshot(cls, snapshot: FvpSnapshot) -> 'FinalVersionPerfectedSession':
        return FinalVersionPerfectedSession(task_priorities = snapshot.task_priorities)

    @classmethod
    def create(cls) -> 'FinalVersionPerfectedSession':
        return FinalVersionPerfectedSession(OrderedDict())



