from domain.todo.todoapp import TodoApp


def reset_fvp_algorithm(name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.reset_fvp_algorithm(todolist_id)
