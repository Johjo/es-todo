import json
import os

from bottle import route, run, template, post, request, redirect, hook, response
import urllib.parse
from web_dependency_list import DependencyListWeb
from hexagon.fvp.domain_model import NothingToDo, ChooseTheTask, DoTheTask
from primary.controller import write, read


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'

@post('/todo')
def create_todolist():
    name = get_string_from_request_post('name')
    write.create_todolist(name)
    return redirect('/todo/' + name)


@post('/todo/<name>/item')
def add_item(name):
    item = get_string_from_request_post('item')
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
def post_reword_task(name, task_id):
    write.reword_task(name=name, task_id=task_id, new_name=get_string_from_request_post('new_name'))
    return redirect(f'/todo/{name}')


@post('/todo/<name>/reset')
def reset_fvp_algorithm(name):
    write.reset_fvp_algorithm(dependencies=DependencyListWeb.get_shared_instance())
    return redirect(f'/todo/{name}')


@route('/todo/<todolist_name>')
def todolist(todolist_name) -> str:
    only_inbox: bool = get_string_from_request_get('only_inbox') == '1'
    context: str = get_string_from_request_get('context')
    response = read.which_task(todolist_name=todolist_name, only_inbox=only_inbox, context=context, dependencies=DependencyListWeb.get_shared_instance())
    number_of_items = read.count_open_items(todolist_name)
    # todo: read step 1: introduce fake reading
    counts_by_context = read.current_contexts(todolist_name)
    match response:
        case NothingToDo():
            return template('nothing',
                            todolist_name=todolist_name, response=response,
                            number_of_items=number_of_items, counts_by_context=counts_by_context, urlencode=urllib.parse.quote)
        case DoTheTask(id=task_id, name=task_name):
            return template('do_the_task',
                            todolist_name=todolist_name,
                            task_name=task_name, task_id=task_id,
                            number_of_items=number_of_items, counts_by_context=counts_by_context, urlencode=urllib.parse.quote)
        case ChooseTheTask(id_1=index_1, name_1=name_1, id_2=index_2, name_2=name_2):
            return template('choose_the_task',
                            todolist_name=todolist_name,
                            index_1=index_1, name_1=name_1,
                            index_2=index_2,
                            name_2=name_2,
                            number_of_items=number_of_items, counts_by_context=counts_by_context, urlencode=urllib.parse.quote)

    return template('todolist', todolist_name=todolist_name, response=response)


def get_string_from_request_get(field_name):
    return request.query.getunicode(field_name)


@route('/')
def index():
    return template('index')


@post('/todo/<name>/item/choose/<chosen_task>/ignore/<ignored_task>')
def choose_and_ignore_task(name, chosen_task, ignored_task):
    write.choose_and_ignore_task(chosen_task, ignored_task, dependencies=DependencyListWeb.get_shared_instance())
    return redirect(f'/todo/{name}')


@route('/todo/<name>/export')
def export_todolist_to_markdown(name):
    markdown = read.export_todo_list_to_markdown(name, dependencies=DependencyListWeb.get_shared_instance())
    number_of_items = read.count_open_items(name)
    return template("export", todolist_name=name, number_of_items=number_of_items, markdown_export=markdown)


@route('/todo/<name>/import')
def import_todolist_from_markdown(name):
    return template("import", todolist_name=name, number_of_items=0)


@post('/todo/<name>/import')
def post_import_todolist_from_markdown(name):
    markdown = get_string_from_request_post('markdown_import')
    write.import_todolist_from_markdown(name, markdown, dependencies=DependencyListWeb.get_shared_instance())
    return redirect(f'/todo/{name}')


def get_string_from_request_post(field_name):
    return request.forms.getunicode(field_name)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    os.environ["PERSISTENCE_MODULE"] = 'eventsourcing.sqlite'
    os.environ["SQLITE_DBNAME"] = 'todo.db'

    host = os.environ["HOST"]
    port = os.environ["PORT"]
    run(reloader=True, host=host, port=port, debug=True)


@route('/rest/todo/<name>/count_tasks')
def count_tasks(name):
    count = read.count_open_items(name)
    return json.dumps({"count": count})
