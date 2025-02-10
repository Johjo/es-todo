from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.hexagon.user.create_todolist import CreateTodolist
from src.primary.use_cases_port import UseCasePort


class UseCasesEmpty(UseCasePort):
    def create_todolist(self) -> CreateTodolist:
        raise NotImplementedError()

    def open_task(self) -> OpenTaskUseCase:
        raise NotImplementedError()
