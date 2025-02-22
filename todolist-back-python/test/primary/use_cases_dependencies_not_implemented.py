from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.port import UseCaseDependenciesPort
from test.hexagon.todolist.write.test_delete_todolist import TodolistDelete


class UseCaseDependenciesNotImplemented(UseCaseDependenciesPort):
    def create_todolist(self) -> TodolistCreate:
        raise NotImplementedError()

    def open_task(self) -> OpenTaskUseCase:
        raise NotImplementedError()

    def delete_todolist(self) -> TodolistDelete:
        raise NotImplementedError()
