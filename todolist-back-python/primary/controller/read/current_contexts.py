# todo read step 2: introduce controller with fake reading
# todo read step 3 : introduce query with fake reading
from domain.todo.todoapp import TodoApp
from hexagon.query.context_query import OpenTaskReader
from test.hexagon.query.test_context_query import TodoContextQuery


class OpenTaskReaderApp(OpenTaskReader):
    def __init__(self, name: str):
        self.app = TodoApp()
        self.name = name

    def all(self) -> list[str]:
        self.app.open_todolist(self.name)
        todolist_id = self.app.open_todolist(self.name)
        return [task.name for task in self.app.all_tasks(todolist_id) if task.done == False]


def current_contexts(name: str):
    task_reader = OpenTaskReaderApp(name)
    contexts = TodoContextQuery(task_reader).all_contexts()
    return contexts
