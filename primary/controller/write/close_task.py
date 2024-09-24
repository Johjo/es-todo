from domain.todo.todoapp import TodoApp


def close_task(item_index, name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.close_item(todolist_id, int(item_index))
