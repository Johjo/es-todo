from domain.todo.todoapp import TodoApp


def which_task(name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    response = app.which_task(todolist_id)
    return response
