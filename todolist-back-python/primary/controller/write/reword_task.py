from domain.todo.todoapp import TodoApp


def reword_task(name, task_id, new_name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.reword_item(todolist_id, int(task_id), new_name)
