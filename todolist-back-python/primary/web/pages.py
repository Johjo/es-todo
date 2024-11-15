from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import quote as urlencode
from uuid import UUID

from bottle import template, Bottle, view, request, redirect  # type: ignore
from bottle_utils import form  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.read.which_task import WhichTaskFilter
from hexagon.shared.type import TaskKey, TodolistName, TaskExecutionDate, TaskName
from primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from primary.controller.read.todolist import TodolistReadController, TaskPresentation, TaskFilter, Include, Word, \
    Exclude
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
def create_todolist():
    todolist_name = get_string_from_request_post("name")
    TodolistWriteController(bottle_config.dependencies).create_todolist(todolist_name)
    return redirect_to_todolist(todolist_name)


@bottle_app.route("/todo/<todolist_name>/import")
@view("import")
def show_import(todolist_name):
    return base_value(todolist_name)


@bottle_app.post("/todo/<todolist_name>/import")
def import_task(todolist_name):
    markdown_import = get_string_from_request_post("markdown_import")
    TodolistWriteController(bottle_config.dependencies).import_many_tasks_from_markdown(todolist_name, markdown_import)
    return redirect_to_todolist(todolist_name)


@bottle_app.route("/todo/<todolist_name>")
def show_todolist(todolist_name):
    task_filter = WhichTaskFilter(todolist_name=todolist_name,
                             include_context=tuple(request.query.getall('include_context')),
                             exclude_context=tuple(request.query.getall('exclude_context')))

    which_task = FinalVersionPerfectedReadController(bottle_config.dependencies).which_task(task_filter=task_filter)
    match which_task:
        case NothingToDo():
            return show_todolist_when_no_task(todolist_name=todolist_name)

        case DoTheTask():
            return show_todolist_when_one_task(todolist_name=todolist_name, do_the_task=which_task)

        case ChooseTheTask():
            return show_todolist_when_two_tasks(todolist_name=todolist_name, choose_the_task=which_task)


def show_todolist_when_no_task(todolist_name):
    return template("nothing", base_value(todolist_name))


def show_todolist_when_one_task(todolist_name: str, do_the_task: DoTheTask):
    task = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, do_the_task.id)
    return template("do_the_task",
                    {**base_value(todolist_name),
                     "task_name": do_the_task.name,
                     "task_id": do_the_task.id,
                     "task": task,
                     }, )


def show_todolist_when_two_tasks(todolist_name: str, choose_the_task: ChooseTheTask):
    task_1 = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, choose_the_task.id_1)
    task_2 = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, choose_the_task.id_2)

    print(task_1, task_2)
    return template("choose_the_task",
                    {**base_value(todolist_name),
                     "name_1": choose_the_task.name_1,
                     "index_1": choose_the_task.id_1,
                     "todolist_name": todolist_name,
                     "index_2": choose_the_task.id_2,
                     "name_2": choose_the_task.name_2,
                     "task_1": task_1,
                     "task_2": task_2,
                     })


@bottle_app.post("/todo/<todolist_name>/item")
def open_task(todolist_name: str):
    task_name = get_string_from_request_post("task_name")
    TodolistWriteController(bottle_config.dependencies).open_task(TodolistName(todolist_name), TaskName(task_name))
    return redirect_to_todolist(todolist_name)


def redirect_to_todolist(todolist_name):
    return redirect(f"/todo/{todolist_name}?{request.query_string}")


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/close")
def close_task(todolist_name: str, task_key: str):
    TodolistWriteController(bottle_config.dependencies).close_task(TodolistName(todolist_name), task_key=TaskKey(UUID(task_key)))
    return redirect_to_todolist(todolist_name)


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/reword")
def reword_task(todolist_name: str, task_key: str):
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.reword_task(todolist_name=TodolistName(todolist_name),
                           task_key=TaskKey(UUID(task_key)),
                           new_name=TaskName(get_string_from_request_post("new_name")))

    return redirect_to_todolist(todolist_name)


@bottle_app.get("/todo/<todolist_name>/item/<task_key>/reword")
def display_reword_task(todolist_name: str, task_key: str):
    controller = TodolistReadController(bottle_config.dependencies)

    task: TaskPresentation = controller.task_by(todolist_name=todolist_name,
                                                task_key=TaskKey(UUID(task_key)))
    return template("reword", {
        "todolist_name": todolist_name,
        "task_id": task_key,
        "query_string": request.query_string,
        "task_name": task.name})


class PostponeForm(form.Form):
    execution_date = form.DateField(label="Date d'execution")


@bottle_app.get("/todo/<todolist_name>/item/<task_key>/postpone")
def display_postpone_task(todolist_name: str, task_key: str):
    postpone_form = PostponeForm()
    return display_form_postpone_task(todolist_name, task_key, postpone_form)


def display_form_postpone_task(todolist_name, task_key, postpone_form):
    controller = TodolistReadController(bottle_config.dependencies)
    task = controller.task_by(todolist_name=todolist_name, task_key=TaskKey(UUID(task_key)))
    return template("postpone", {
        "todolist_name": todolist_name,
        "task_id": task_key,
        "query_string": request.query_string,
        "task": task,
        "form": postpone_form,
    })


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/postpone")
def postpone(todolist_name: str, task_key: str):
    postpone_form = PostponeForm(request.forms)
    if postpone_form.is_valid():
        controller = TodolistWriteController(bottle_config.dependencies)
        date_as_str = request.forms.getunicode("execution_date")
        controller.postpone_task(
            name=TodolistName(todolist_name),
            key=TaskKey(UUID(task_key)),
            execution_date=TaskExecutionDate(datetime.strptime(date_as_str, "%Y-%m-%d").date()))
        return redirect_to_todolist(todolist_name)
    return display_form_postpone_task(todolist_name, task_key, postpone_form)


@bottle_app.get("/todo/<todolist_name>/export")
@view("export")
def display_export_as_markdown(todolist_name: str):
    markdown = TodolistReadController(dependencies=bottle_config.dependencies).to_markdown(todolist_name=todolist_name)

    return {**base_value(todolist_name), "markdown_export": markdown, }


@bottle_app.post('/todo/<todolist_name>/item/choose/<chosen_task>/ignore/<ignored_task>')
def choose_and_ignore_task(todolist_name, chosen_task, ignored_task):
    TodolistWriteController(bottle_config.dependencies).choose_and_ignore_task(chosen_task=chosen_task,
                                                                               ignored_task=ignored_task)
    return redirect_to_todolist(todolist_name)


@bottle_app.post('/todo/<todolist_name>/item/<task_key>/cancel_priority')
def cancel_priority(todolist_name, task_key):
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.cancel_priority(task_key=TaskKey(UUID(task_key)))
    return redirect_to_todolist(todolist_name)


@bottle_app.post('/todo/<todolist_name>/reset')
def reset_all_priorities(todolist_name):
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.reset_all_priorities()
    return redirect_to_todolist(todolist_name)


def get_string_from_request_post(field_name: str) -> str:
    return request.forms.getunicode(field_name)


def base_value(todolist_name: str) -> dict[str, Any]:
    return {
        "todolist_name": todolist_name,
        "query_string": request.query_string,
        "number_of_items": "xxxx_number_of_items",
        "counts_by_context": TodolistReadController(bottle_config.dependencies).counts_by_context(todolist_name),
        "included_context": request.query.getall("include_context"),
        "excluded_context": request.query.getall("exclude_context"),
        "urlencode": urlencode,
    }
