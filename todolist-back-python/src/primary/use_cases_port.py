from abc import ABC, abstractmethod
from typing import Protocol

from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.hexagon.user.create_todolist import CreateTodolist


class UseCasePort(ABC):
    @abstractmethod
    def create_todolist(self) -> CreateTodolist:
        pass

    @abstractmethod
    def open_task(self) -> OpenTaskUseCase:
        pass
