from domain.todo.todoapp import TodoApp


def add_task(item, name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.add_item(todolist_id, item)
