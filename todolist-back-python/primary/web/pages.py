import urllib
from dataclasses import dataclass

from bottle import template, Bottle, view, response, request  # type: ignore

from hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.read.which_task import TaskFilter
from primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from primary.controller.read.todolist import TodolistReadController, Task
from dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController

bottle_app = Bottle()


@dataclass
class BottleConfig:
    dependencies: Dependencies


bottle_config = BottleConfig(dependencies=Dependencies.create_empty())


@bottle_app.route("/")
@view("index")
def index():
    controller = TodolistReadController(bottle_config.dependencies)
    return {"todolist_name_set": controller.all_todolist_by_name()}


@bottle_app.post("/todo")
@view("index")
def create_todolist():
    todolist_name = get_string_from_request_post("name")
    TodolistWriteController(bottle_config.dependencies).create_todolist(todolist_name)
    return {"todolist_name_set": TodolistReadController(bottle_config.dependencies).all_todolist_by_name()}


@bottle_app.route("/todo/<todolist_name>")
def show_todolist(todolist_name):
    task_filter = TaskFilter(todolist_name=todolist_name)  # todo mutate this

    which_task = FinalVersionPerfectedReadController(bottle_config.dependencies).which_task(task_filter=task_filter)
    match which_task:
        case NothingToDo():
            return show_todolist_when_no_task(todolist_name=todolist_name)

        case DoTheTask():
            return show_todolist_when_one_task(todolist_name=todolist_name, do_the_task=which_task)

        case ChooseTheTask():
            return show_todolist_when_two_tasks(todolist_name=todolist_name, choose_the_task=which_task)


def show_todolist_when_no_task(todolist_name):
    return template("nothing", {
        "todolist_name": todolist_name,
        "query_string": "xxxx_query_string",
        "number_of_items": "xxxx_number_of_items",
        "counts_by_context": {"xxxx1": "xxxx2"},
        "urlencode": urllib.parse.quote,
    })


def show_todolist_when_one_task(todolist_name: str, do_the_task: DoTheTask):
    return template("do_the_task", {
        "task_name": do_the_task.name,
        "task_id": do_the_task.id,
        "todolist_name": todolist_name,
        "query_string": "xxxx_query_string",
        "number_of_items": "xxxx_number_of_items",
        "counts_by_context": {"xxxx1": "xxxx2"},
        "urlencode": urllib.parse.quote}, )


def show_todolist_when_two_tasks(todolist_name: str, choose_the_task: ChooseTheTask):
    return template("choose_the_task", {
        "name_1": choose_the_task.name_1,
        "index_1": choose_the_task.id_1,
        "todolist_name": todolist_name,
        "index_2": choose_the_task.id_2,
        "name_2": choose_the_task.name_2,
        "query_string": "xxxx_query_string",
        "number_of_items": "xxxx_number_of_items",
        "counts_by_context": {"xxxx1": "xxxx2"},
        "urlencode": urllib.parse.quote,
    })


@bottle_app.post("/todo/<todolist_name>/item")
def open_task(todolist_name: str):
    task_name = get_string_from_request_post("task_name")
    TodolistWriteController(bottle_config.dependencies).open_task(todolist_name, task_name)
    return show_todolist(todolist_name)


@bottle_app.get("/todo/<todolist_name>/item/<task_key>/reword")
def display_reword_task(todolist_name: str, task_key: int):
    pass
    task: Task = TodolistReadController(bottle_config.dependencies).task_by(todolist_name=todolist_name, task_key=int(task_key))
    return template("reword", {
        "todolist_name": todolist_name,
        "task_id": task_key,
        "query_string": "xxxx_query_string",
        "task_name": task.name})


def get_string_from_request_post(field_name):
    return request.forms.getunicode(field_name)
