from domain.todo.todoapp import TodoApp


def create_todolist(name):
    app = TodoApp()
    app.start_todolist(name)
