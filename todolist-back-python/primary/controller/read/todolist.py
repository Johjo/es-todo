from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import cast
from uuid import UUID

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from shared.filter import TextFilter


@dataclass(frozen=True)
class Criterion:
    pass


@dataclass
class Category:
    pass


@dataclass(frozen=True)
class Include(Criterion):
    category: Category


@dataclass(frozen=True)
class Exclude(Criterion):
    category: Category


@dataclass
class Word(Category):
    value: str

@dataclass
class WithoutDate(Category):
    pass


@dataclass(frozen=True, eq=True)
class TaskFilter:
    todolist_name: TodolistName
    criteria: tuple[Criterion, ...] = ()

    def include(self, task_name: str) -> bool:
        include_context: set[str] = set()
        exclude_context: set[str] = set()

        for criterion in self.criteria:
            match criterion:
                case Include(Word(word)):
                    include_context.add(word)
                case Exclude(Word(word)):
                    exclude_context.add(word)
                case Exclude(WithoutDate()):
                    pass
                case _:
                    raise ValueError(f"Unknown criterion {criterion}")

        text_filter = TextFilter(included_words=tuple(include_context), excluded_words=tuple(exclude_context))
        return text_filter.include(task_name)

    @classmethod
    def create(cls, todolist_name: TodolistName, *criteria: Criterion) -> 'TaskFilter':
        return TaskFilter(todolist_name=todolist_name, criteria=tuple(criteria))

@dataclass(frozen=True)
class TaskPresentation:
    key: UUID
    name: str
    is_open: bool
    execution_date: date | None


class TodolistSetReadPort(ABC):
    @abstractmethod
    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        pass

    @abstractmethod
    def all_by_name(self) -> list[TodolistName]:
        pass

    @abstractmethod
    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        pass

    @abstractmethod
    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        pass

    @abstractmethod
    def all_tasks_postponed_task(self, todolist_name: str, reference_date: date) -> list[TaskPresentation]:
        pass


class CalendarPort(ABC):
    @abstractmethod
    def today(self) -> date:
        pass


class TodolistReadController:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def all_todolist_by_name(self) -> list[str]:
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return cast(list[str], todolist_set.all_by_name())

    def task_by(self, todolist_name: str, task_key: TaskKey) -> TaskPresentation:
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return todolist_set.task_by(todolist_name=todolist_name, task_key=task_key)

    def counts_by_context(self, todolist_name: str):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        context = todolist_set.counts_by_context(todolist_name=TodolistName(todolist_name))
        return sorted(context)

    def to_markdown(self, todolist_name: str):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return to_markdown(todolist_set.all_tasks(TaskFilter(todolist_name=TodolistName(todolist_name))))

    def all_task(self, task_filter: TaskFilter):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        return todolist_set.all_tasks(task_filter=task_filter)

    def all_tasks_postponed_task(self, todolist_name: str):
        todolist_set: TodolistSetReadPort = self.dependencies.get_adapter(TodolistSetReadPort)
        calendar : CalendarPort = self.dependencies.get_adapter(CalendarPort)
        return todolist_set.all_tasks_postponed_task(todolist_name=todolist_name, reference_date=calendar.today())


def to_markdown(tasks: list[TaskPresentation]) -> str:
    def task_to_markdown(task: TaskPresentation) -> str:
        return f"- [{" " if task.is_open else "x"}] {task.name}"

    return "\n".join([task_to_markdown(task) for task in tasks])
