from dependencies import Dependencies
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class RewordTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name, key, new_wording):
        update = lambda todolist: todolist.reword_task(key, new_wording)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'RewordTask':
        return RewordTask(dependencies.get_adapter(TodolistSetPort))
