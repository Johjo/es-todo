from abc import abstractmethod, ABC
from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src.hexagon.shared.type import TodolistKey


class TaskPresentation(BaseModel):
    key: UUID
    name: str
    open: bool
    execution_date: date | None


class AllTasksPresentation(BaseModel):
    tasks: list[TaskPresentation]


class AllTaskPort(ABC):
    @abstractmethod
    def all_tasks(self, todolist_key: TodolistKey) -> AllTasksPresentation:
        pass
