from domain.todo.todoapp import TodoApp


def get_task(name, task_id):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    task = app.get_task(todolist_id, int(task_id))
    return task
