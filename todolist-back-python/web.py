import json
import os
import urllib.parse

from bottle import template, request, redirect, response

from hexagon.fvp.domain_model import NothingToDo, ChooseTheTask, DoTheTask
from hexagon.fvp.port import FvpSessionRepository
from hexagon.fvp.read.which_task import TaskReader
from primary.controller import write, read
from primary.controller.read.which_task import DependencyList
from primary.web import app
from secondary.fvp.json_session_repository import JsonSessionRepository
from secondary.fvp.task_reader_todolist import TaskReaderTodolist
from utils import SharedInstanceBuiltIn
from web_dependency_list import DependencyListWeb


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'


@app.post('/todo')
def create_todolist():
    name = get_string_from_request_post('name')
    write.create_todolist(name)
    return redirect_to_index(name)


@app.post('/todo/<name>/item')
def add_item(name):
    item = get_string_from_request_post('item')
    write.add_task(item, name)
    return redirect_to_index(name)


@app.post('/todo/<name>/item/<item_index>/close')
def close_item(name, item_index):
    write.close_task(item_index, name)
    return redirect_to_index(name)


@app.route('/todo/<name>/item/<task_id>/reword')
def reword_task(name, task_id):
    task = read.get_task(name, task_id)
    return template('reword', todolist_name=name, task_id=task_id, task_name=task.name,
                    query_string=request.query_string)


@app.post('/todo/<name>/item/<task_id>/reword')
def post_reword_task(name, task_id):
    write.reword_task(name=name, task_id=task_id, new_name=get_string_from_request_post('new_name'))
    return redirect_to_index(name)


@app.post('/todo/<name>/reset')
def reset_fvp_algorithm(name):
    write.reset_fvp_algorithm(dependencies=DependencyListWeb.get_shared_instance())
    return redirect_to_index(name)


@app.route('/todo/<todolist_name>')
def todolist(todolist_name) -> str:
    print(f"request.urlparts : {request.urlparts}")
    print(f"request.urlparts[2] : {request.urlparts[2]}")
    print(f"request.urlparts[3] : {request.urlparts[3]}")
    print(f"request.query_string : {request.query_string}")

    only_inbox: bool = get_string_from_request_get('only_inbox') == '1'
    context: str = get_string_from_request_get('context')
    which_task_response = read.which_task_old(todolist_name=todolist_name, only_inbox=only_inbox, context=context,
                                              dependencies=DependencyListWeb.get_shared_instance())
    number_of_items = read.count_open_items(todolist_name)
    # todo: read step 1: introduce fake reading
    counts_by_context = read.current_contexts(todolist_name)
    match which_task_response:
        case NothingToDo():
            return template('nothing',
                            todolist_name=todolist_name, response=which_task_response,
                            number_of_items=number_of_items, counts_by_context=counts_by_context,
                            urlencode=urllib.parse.quote,
                            query_string=request.query_string)
        case DoTheTask(id=task_id, name=task_name):
            return template('do_the_task',
                            todolist_name=todolist_name,
                            task_name=task_name, task_id=task_id,
                            number_of_items=number_of_items, counts_by_context=counts_by_context,
                            urlencode=urllib.parse.quote,
                            query_string=request.query_string)
        case ChooseTheTask(id_1=index_1, name_1=name_1, id_2=index_2, name_2=name_2):
            return template('choose_the_task',
                            todolist_name=todolist_name,
                            index_1=index_1, name_1=name_1,
                            index_2=index_2,
                            name_2=name_2,
                            number_of_items=number_of_items, counts_by_context=counts_by_context,
                            urlencode=urllib.parse.quote)

    return template('todolist', todolist_name=todolist_name, response=which_task_response)


def get_string_from_request_get(field_name):
    return request.query.getunicode(field_name)


@app.route('/')
def index():
    return template('index')


@app.post('/todo/<name>/item/choose/<chosen_task>/ignore/<ignored_task>')
def choose_and_ignore_task(name, chosen_task, ignored_task):
    redirect_url = get_string_from_request_post("redirect")
    write.choose_and_ignore_task(chosen_task, ignored_task, dependencies=DependencyListWeb.get_shared_instance())
    return redirect_to_index(name)


def redirect_to_index(name):
    return redirect(f'/todo/{name}?' + request.query_string)


@app.route('/todo/<name>/export')
def export_todolist_to_markdown(name):
    markdown = read.export_todo_list_to_markdown(name, dependencies=DependencyListWeb.get_shared_instance())
    number_of_items = read.count_open_items(name)
    return template("export",
                    todolist_name=name, number_of_items=number_of_items,
                    markdown_export=markdown,
                    counts_by_context=read.current_contexts(name),
                    query_string=request.query_string, urlencode=urllib.parse.quote)


@app.route('/todo/<name>/import')
def import_todolist_from_markdown(name):
    return template("import", todolist_name=name, number_of_items=0, counts_by_context=read.current_contexts(name),
                    query_string=request.query_string, urlencode=urllib.parse.quote)


@app.post('/todo/<name>/import')
def post_import_todolist_from_markdown(name):
    markdown = get_string_from_request_post('markdown_import')
    write.import_todolist_from_markdown(name, markdown, dependencies=DependencyListWeb.get_shared_instance())
    return redirect_to_index(name)


def get_string_from_request_post(field_name):
    return request.forms.getunicode(field_name)


@app.route('/rest/todo/<name>/count_tasks')
def count_tasks(name):
    count = read.count_open_items(name)
    return json.dumps({"count": count})


class DependencyListNew(SharedInstanceBuiltIn):
    pass


@app.route('/rest/todo/<name>')
def rest_todolist(name):
    # todo: read step 1: introduce fake reading
    # todo read step 2: introduce controller with fake reading
    # todo read step 3 : introduce query with fake reading
    # todo read step 4: introduce test around query
    todolist = read.todolist(name, dependencies=DependencyListNew.get_shared_instance())
    return json.dumps(todolist.to_dict())


class DependencyListForWeb(DependencyList):
    def fvp_session_repository_for_which_task_query(self) -> FvpSessionRepository:
        return JsonSessionRepository("session_fvp.json")

    def task_reader_for_which_task_query(self, todolist_name: str, only_inbox: bool, context: str) -> TaskReader:
        return TaskReaderTodolist(todolist_name=todolist_name, only_inbox=only_inbox, context=context)


if __name__ == '__main__':
    from dotenv import load_dotenv

    app.dependencies = DependencyListForWeb()
    load_dotenv()

    os.environ["PERSISTENCE_MODULE"] = 'eventsourcing.sqlite'
    os.environ["SQLITE_DBNAME"] = 'todo.db'

    host = os.environ["HOST"]
    port = os.environ["PORT"]
    app.run(reloader=True, host=host, port=port, debug=True)
