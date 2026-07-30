from expression import Result, Nothing

from dependencies import Dependencies
from hexagon.shared.type import TaskName, TaskOpen, TodolistName
from hexagon.todolist.aggregate import Task, TodolistAggregate
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class OpenTaskUseCase:
    def __init__(self, todolist_set: TodolistSetPort, task_key_generator: TaskKeyGeneratorPort):
        self._todolist_set = todolist_set
        self._task_key_generator = task_key_generator

    def execute(self, todolist_name: TodolistName, name: TaskName) -> Result[None, str]:
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.open_task(Task(key=self._task_key_generator.generate(), name=name, is_open=TaskOpen(True), execution_date=Nothing))
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'OpenTaskUseCase':
        return OpenTaskUseCase(dependencies.get_adapter(TodolistSetPort), dependencies.get_adapter(TaskKeyGeneratorPort))
