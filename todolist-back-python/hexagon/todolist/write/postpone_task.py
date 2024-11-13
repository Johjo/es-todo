from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TaskKey, TaskExecutionDate
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class PostPoneTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: TodolistName, key: TaskKey, execution_date: TaskExecutionDate):
        update = lambda todolist: todolist.postpone_task(key, execution_date)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)

    @staticmethod
    def factory(dependencies: Dependencies) -> 'PostPoneTask':
        todolist_set = dependencies.get_adapter(TodolistSetPort)
        return PostPoneTask(todolist_set)
