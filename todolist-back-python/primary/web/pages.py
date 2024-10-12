from dataclasses import dataclass

from bottle import template, Bottle, view, response  # type: ignore

from primary.controller.read.todolist import TodolistReadController
from primary.controller.write.dependencies import Dependencies

bottle_app = Bottle()

@dataclass
class BottleConfig:
    dependencies: Dependencies

bottle_config = BottleConfig(dependencies=Dependencies.create_empty())

@bottle_app.route("/")
@view("index")
def index():
    print(bottle_config.dependencies.adapter_factory)
    controller = TodolistReadController(bottle_config.dependencies)
    return {"todolist_name_set": controller.all_todolist_by_name()}

