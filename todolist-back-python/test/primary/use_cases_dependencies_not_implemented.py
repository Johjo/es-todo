from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.port import UseCaseDependenciesPort


class UseCaseDependenciesNotImplemented(UseCaseDependenciesPort):
    def create_todolist(self) -> TodolistCreate:
        raise NotImplementedError()

    def open_task(self) -> OpenTaskUseCase:
        raise NotImplementedError()
