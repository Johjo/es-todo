from abc import ABC, abstractmethod

from src.hexagon.todolist.port import TodolistSetPort
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.hexagon.user.create_todolist import CreateTodolist
from src.hexagon.user.port import UserRepositoryPort
from src.infra.memory import Memory
from src.primary.rest import start_app
from src.primary.use_cases_port import UseCasePort
from src.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from src.secondary.user.user_repository_in_memory import UserRepositoryInMemory


class AdapterPort(ABC):
    @abstractmethod
    def user_repository(self) -> UserRepositoryPort:
        pass

    @abstractmethod
    def todolist_set(self) -> TodolistSetPort:
        pass


class InfrastructurePort(ABC):
    @abstractmethod
    def todolist_memory(self) -> Memory:
        pass


class AdapterForDemo(AdapterPort):
    def __init__(self, infrastructure: InfrastructurePort):
        self._infrastructure = infrastructure

    def user_repository(self) -> UserRepositoryPort:
        return UserRepositoryInMemory()

    def todolist_set(self) -> TodolistSetPort:
        return TodolistSetInMemory(memory=self._infrastructure.todolist_memory(), user_key="")


class UseCases(UseCasePort):
    def __init__(self, adapters: AdapterPort) -> None:
        self._adapters = adapters

    def create_todolist(self) -> CreateTodolist:
        return CreateTodolist(user_repository=self._adapters.user_repository())

    def open_task(self) -> OpenTaskUseCase:
        return OpenTaskUseCase(todolist_set=self._adapters.todolist_set())


class InfrastructureForDemo(InfrastructurePort):
    def __init__(self) -> None:
        self._memory = Memory()

    def todolist_memory(self) -> Memory:
        return self._memory


app = start_app(UseCases(adapters=AdapterForDemo(infrastructure=InfrastructureForDemo())))
