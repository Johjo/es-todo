import os

from bottle import route, run, template, post, request, redirect

from domain.presentation import NothingToDo, DoTheTask, ChooseTheTask
from primary.controller import write, read


@post('/todo')
def create_todolist():
    name = get_string_from_request('name')
    write.create_todolist(name)
    return redirect('/todo/' + name)


@post('/todo/<name>/item')
def add_item(name):
    item = get_string_from_request('item')
    write.add_task(item, name)
    return redirect(f'/todo/{name}')


@post('/todo/<name>/item/<item_index>/close')
def close_item(name, item_index):
    write.close_task(item_index, name)
    return redirect(f'/todo/{name}')


@route('/todo/<name>/item/<task_id>/reword')
def reword_task(name, task_id):
    task = read.get_task(name, task_id)
    return template('reword', todolist_name=name, task_id=task_id, task_name=task.name)


@post('/todo/<name>/item/<task_id>/reword')
def reword_task(name, task_id):
    write.reword_task(name=name, task_id=task_id, new_name=get_string_from_request('new_name'))
    return redirect(f'/todo/{name}')


@post('/todo/<name>/reset')
def reset_fvp_algorithm(name):
    write.reset_fvp_algorithm(name)
    return redirect(f'/todo/{name}')


@route('/todo/<name>')
def todolist(name):
    response = read.which_task(name)
    number_of_items = read.count_open_items(name)

    match response:
        case NothingToDo():
            return template('nothing', todolist_name=name, response=response, number_of_items=number_of_items)
        case DoTheTask(index=task_id, name=task_name):
            return template('do_the_task', todolist_name=name, task_name=task_name, task_id=task_id,
                            number_of_items=number_of_items)
        case ChooseTheTask(index_1=index_1, name_1=name_1, index_2=index_2, name_2=name_2):
            return template('choose_the_task', todolist_name=name, index_1=index_1, name_1=name_1, index_2=index_2,
                            name_2=name_2, number_of_items=number_of_items)

    return template('todolist', todolist_name=name, response=response)


@route('/')
def index():
    return template('index')


@post('/todo/<name>/item/choose/<chosen_task>/ignore/<ignored_task>')
def choose_and_ignore_task(name, chosen_task, ignored_task):
    write.choose_and_ignore_task(chosen_task, ignored_task, name)
    return redirect(f'/todo/{name}')


@route('/todo/<name>/export')
def export_todolist_to_markdown(name):
    return template("export", todolist_name=name, number_of_items=read.count_open_items(name),
                    markdown_export=read.export_todo_list_to_markdown(name))


@route('/todo/<name>/import')
def import_todolist_from_markdown(name):
    return template("import", todolist_name=name, number_of_items=0)


@post('/todo/<name>/import')
def import_todolist_from_markdown(name):
    markdown = get_string_from_request('markdown_import')
    write.import_todolist_from_markdown(name, markdown)
    return redirect(f'/todo/{name}')


def get_string_from_request(field_name):
    return request.forms.getunicode(field_name)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    os.environ["PERSISTENCE_MODULE"] = 'eventsourcing.sqlite'
    os.environ["SQLITE_DBNAME"] = 'todo.db'

    host = os.environ["HOST"]
    port = os.environ["PORT"]
    run(reloader=True, host=host, port=port, debug=True)
