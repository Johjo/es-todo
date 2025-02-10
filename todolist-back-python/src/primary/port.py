from abc import ABC, abstractmethod

from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.todolist.read.port import AllTaskPort


class UseCaseDependenciesPort(ABC):
    @abstractmethod
    def create_todolist(self) -> TodolistCreate:
        pass

    @abstractmethod
    def open_task(self) -> OpenTaskUseCase:
        pass


class QueryDependenciesPort(ABC):
    @abstractmethod
    def all_tasks(self) -> AllTaskPort:
        pass
