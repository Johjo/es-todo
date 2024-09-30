from domain.todo.todoapp import TodoApp


def count_open_items(name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    number_of_items = len(app.get_open_items(todolist_id))
    return number_of_items
