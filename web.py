import os

from bottle import route, run, template, post, request, redirect

from domain.presentation import NothingToDo, DoTheTask, ChooseTheTask
from domain.todoapp import TodoApp

@post('/todo')
def create_todolist():
    name = request.forms.get('name')
    app = TodoApp()
    app.start_todolist(name)
    return redirect('/todo/' + name)

@post('/todo/<name>/item')
def add_item(name):
    item = request.forms.get('item')
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.add_item(todolist_id, item)
    return redirect(f'/todo/{name}')

@post('/todo/<name>/item/<item_index>/close')
def close_item(name, item_index):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.close_item(todolist_id, int(item_index))
    return redirect(f'/todo/{name}')

@route('/todo/<name>')
def todolist(name):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    response = app.which_task(todolist_id)

    match response:
        case NothingToDo():
            return template('nothing', todolist_name=name, response=response)
        case DoTheTask(index=task_id, name=task_name):
            return template('do_the_task', todolist_name=name, task_name=task_name, task_id=task_id)
        case ChooseTheTask(index_1=index_1, name_1=name_1, index_2=index_2, name_2=name_2):
            return template('choose_the_task', todolist_name=name, index_1=index_1, name_1=name_1, index_2=index_2, name_2=name_2)

    return template('todolist', todolist_name=name, response=response)

@route('/')
def index():
    return template('index')

@post('/todo/<name>/item/choose/<chosen_task>/ignore/<ignored_task>')
def choose_and_ignore_task(name, chosen_task, ignored_task):
    app = TodoApp()
    todolist_id = app.open_todolist(name)
    app.choose_and_ignore_task(todolist_id=todolist_id, chosen_index=int(chosen_task), ignored_index=int(ignored_task))
    return redirect(f'/todo/{name}')


if __name__ == '__main__':
    os.environ["PERSISTENCE_MODULE"] = 'eventsourcing.sqlite'
    os.environ["SQLITE_DBNAME"] = 'todo.db'

    run(reloader=True)