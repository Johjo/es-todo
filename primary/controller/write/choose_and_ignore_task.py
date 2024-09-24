from domain.todo.todoapp import TodoApp


def choose_and_ignore_task(chosen_task, ignored_task, name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.choose_and_ignore_task(todolist_id=todolist_id, chosen_index=int(chosen_task), ignored_index=int(ignored_task))
