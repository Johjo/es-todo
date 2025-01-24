from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Any
from urllib.parse import quote as urlencode
from uuid import UUID

from bottle import template, Bottle, view, request, redirect, static_file, auth_basic  # type: ignore
from bottle_utils import form  # type: ignore

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from src.hexagon.fvp.read.which_task import WhichTaskFilter
from src.hexagon.shared.type import TaskKey, TodolistName, TaskExecutionDate, TaskName
from src.primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from src.primary.controller.read.todolist import TodolistReadController, TaskPresentation
from src.primary.controller.write.todolist import TodolistWriteController
from src.shared.const import USER_KEY

bottle_app = Bottle()


@dataclass
class BottleConfig:
    dependencies: Dependencies


bottle_config = BottleConfig(dependencies=Dependencies.create_empty())


def is_authenticated_user(user, password):
    return user == password


@bottle_app.route("/todo")
@bottle_app.route("/")
@auth_basic(is_authenticated_user)
@view("index")
def index():
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    controller = TodolistReadController(bottle_config.dependencies)
    return {"todolist_name_set": controller.all_todolist_by_name()}


@bottle_app.post("/todo")
@auth_basic(is_authenticated_user)
def create_todolist():
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    todolist_name = get_string_from_request_post("name")
    TodolistWriteController(bottle_config.dependencies).create_todolist(TodolistName(todolist_name))
    return redirect_to_todolist(todolist_name)


@bottle_app.route("/todo/<todolist_name>/import")
@view("import")
@auth_basic(is_authenticated_user)
def show_import(todolist_name):
    return base_value(todolist_name)


@bottle_app.route("/todo/<todolist_name>/calendar")
@view("calendar")
@auth_basic(is_authenticated_user)
def show_calendar(todolist_name):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    tasks = TodolistReadController(bottle_config.dependencies).all_tasks_postponed_task(todolist_name)
    return {**base_value(todolist_name),
            "tasks":tasks}


@bottle_app.post("/todo/<todolist_name>/import")
@auth_basic(is_authenticated_user)
def import_task(todolist_name):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    markdown_import = get_string_from_request_post("markdown_import")
    TodolistWriteController(bottle_config.dependencies).import_many_tasks_from_markdown(todolist_name, markdown_import)
    return redirect_to_todolist(todolist_name)


@bottle_app.route("/todo/<todolist_name>")
@auth_basic(is_authenticated_user)
def show_todolist(todolist_name: str) -> str:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    task_filter = WhichTaskFilter(todolist_name=TodolistName(todolist_name),
                                  include_context=tuple(request.query.getall('include_context')),
                                  exclude_context=tuple(request.query.getall('exclude_context')),
                                  reference_date=date(2050, 10, 17))

    controller = FinalVersionPerfectedReadController(bottle_config.dependencies)
    which_task = controller.which_task(
        todolist_name=todolist_name,
        include_context=tuple(request.query.getall('include_context')),
        exclude_context=tuple(request.query.getall('exclude_context')),
        task_filter=task_filter)

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
    task = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, do_the_task.key)
    return template("do_the_task",
                    {**base_value(todolist_name),
                     "task_name": task.name,
                     "task_id": task.key,
                     "task": task,
                     }, )


def show_todolist_when_two_tasks(todolist_name: str, choose_the_task: ChooseTheTask):
    task_1 = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, choose_the_task.main_task_key)
    task_2 = TodolistReadController(bottle_config.dependencies).task_by(todolist_name, choose_the_task.secondary_task_key)

    return template("choose_the_task",
                    {**base_value(todolist_name),
                     "todolist_name": todolist_name,
                     "task_1": task_1,
                     "task_2": task_2,
                     })


@bottle_app.post("/todo/<todolist_name>/item")
@auth_basic(is_authenticated_user)
def open_task(todolist_name: str):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    task_name = get_string_from_request_post("task_name")
    TodolistWriteController(bottle_config.dependencies).open_task(TodolistName(todolist_name), TaskName(task_name))
    return redirect_to_todolist(todolist_name)


def redirect_to_todolist(todolist_name) -> str:
    return redirect(f"/todo/{todolist_name}?{request.query_string}")


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/close")
@auth_basic(is_authenticated_user)
def close_task(task_key: str, todolist_name: str):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    TodolistWriteController(bottle_config.dependencies).close_task(TodolistName(todolist_name), task_key=TaskKey(UUID(task_key)))
    return redirect_to_todolist(todolist_name)


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/reword")
@auth_basic(is_authenticated_user)
def reword_task(todolist_name: str, task_key: str) -> str:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.reword_task(todolist_name=TodolistName(todolist_name),
                           task_key=TaskKey(UUID(task_key)),
                           new_name=TaskName(get_string_from_request_post("new_name")))

    return redirect_to_todolist(todolist_name)


@bottle_app.get("/todo/<todolist_name>/item/<task_key>/reword")
@auth_basic(is_authenticated_user)
def display_reword_task(todolist_name: str, task_key: str) -> str:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
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
@auth_basic(is_authenticated_user)
def display_postpone_task(todolist_name: str, task_key: str) -> str:
    postpone_form = PostponeForm()
    return display_form_postpone_task(todolist_name, task_key, postpone_form)


def display_form_postpone_task(todolist_name, task_key, postpone_form) -> str:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
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
@auth_basic(is_authenticated_user)
def postpone(todolist_name: str, task_key: str) -> str:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
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


@bottle_app.post("/todo/<todolist_name>/item/<task_key>/tomorrow")
@auth_basic(is_authenticated_user)
def postpone_to_tomorrow(todolist_name: str, task_key: str) -> str:
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.postpone_task_to_tomorrow(name=TodolistName(todolist_name), key=TaskKey(UUID(task_key)))
    return redirect_to_todolist(todolist_name)

    # bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    # postpone_form = PostponeForm(request.forms)
    # if postpone_form.is_valid():
    #     controller = TodolistWriteController(bottle_config.dependencies)
    #     date_as_str = request.forms.getunicode("execution_date")
    #     controller.postpone_task(
    #         name=TodolistName(todolist_name),
    #         key=TaskKey(UUID(task_key)),
    #         execution_date=TaskExecutionDate(datetime.strptime(date_as_str, "%Y-%m-%d").date()))
    #     return redirect_to_todolist(todolist_name)
    # return display_form_postpone_task(todolist_name, task_key, postpone_form)


@bottle_app.get("/todo/<todolist_name>/export")
@view("export")
@auth_basic(is_authenticated_user)
def display_export_as_markdown(todolist_name: str) -> dict:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    markdown = TodolistReadController(dependencies=bottle_config.dependencies).to_markdown(todolist_name=todolist_name)

    return {**base_value(todolist_name), "markdown_export": markdown, }


def authenticate(dependencies: Dependencies, user: str) -> Dependencies:
    return dependencies.feed_data(data_name=USER_KEY, value=user)


@bottle_app.post('/todo/<todolist_name>/item/choose/<chosen_task>/ignore/<ignored_task>')
@auth_basic(is_authenticated_user)
def choose_and_ignore_task(todolist_name: str, chosen_task:  str, ignored_task:str):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    TodolistWriteController(bottle_config.dependencies).choose_and_ignore_task(chosen_task=TaskKey(UUID(chosen_task)),
                                                                               ignored_task=TaskKey(UUID(ignored_task)))
    return redirect_to_todolist(todolist_name)


@bottle_app.post('/todo/<todolist_name>/item/<task_key>/cancel_priority')
@auth_basic(is_authenticated_user)
def cancel_priority(todolist_name, task_key):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.cancel_priority(task_key=TaskKey(UUID(task_key)))
    return redirect_to_todolist(todolist_name)


@bottle_app.post('/todo/<todolist_name>/reset')
@auth_basic(is_authenticated_user)
def reset_all_priorities(todolist_name):
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    controller = TodolistWriteController(bottle_config.dependencies)
    controller.reset_all_priorities()
    return redirect_to_todolist(todolist_name)


@bottle_app.get('/static/<filename:path>')
def static(filename: str) -> Any:
    root : str = bottle_config.dependencies.get_path("static_path")
    return static_file(filename, root=Path(root).absolute())





def get_string_from_request_post(field_name: str) -> str:
    return str(request.forms.getunicode(field_name))


def base_value(todolist_name: str) -> dict[str, Any]:
    bottle_config.dependencies = authenticate(dependencies=bottle_config.dependencies, user=request.auth[0])
    return {
        "todolist_name": todolist_name,
        "query_string": request.query_string,
        "number_of_items": "xxxx_number_of_items",
        "counts_by_context": TodolistReadController(bottle_config.dependencies).counts_by_context(todolist_name),
        "included_context": request.query.getall("include_context"),
        "excluded_context": request.query.getall("exclude_context"),
        "urlencode": urlencode,
    }
