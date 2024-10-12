from dataclasses import dataclass

from bottle import template, Bottle, view, response, request  # type: ignore

from primary.controller.read.todolist import TodolistReadController
from primary.controller.write.dependencies import Dependencies
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
# @view("index")
def show_todolist(todolist_name):
    return template("nothing", {
        "todolist_name": todolist_name,
        "query_string":"", # todo: fill query string
        "number_of_items":0, # todo fill number of items
        "counts_by_context": {}, # todo fill counts by context

    })

def get_string_from_request_post(field_name):
    return request.forms.getunicode(field_name)
