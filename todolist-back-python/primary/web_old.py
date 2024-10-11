import json

from bottle import Bottle, request  # type: ignore

from primary.controller import read

app = Bottle()


@app.route('/rest/todo/<todolist_name>/which_task', method='GET')
def which_task(todolist_name: str) -> str:
    only_inbox: bool = get_string_from_request_get('only_inbox') == '1'
    context: str = get_string_from_request_get('context')
    dependencies = app.dependencies
    response = read.which_task(dependencies, only_inbox=only_inbox, context=context, todolist_name=todolist_name)
    return json.dumps(response)


def get_string_from_request_get(field_name):
    return request.query.getunicode(field_name)
