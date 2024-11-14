from typing import Any

from hexagon.fvp.read.which_task import TaskFilter
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import Task
from test.fixture import TodolistBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class CleanResponse:
    def __init__(self, response: Any) :
        self._response = response

    def location(self) -> str:
        full_location = self._response.headers['Location']
        without_protocol = full_location.split("//")[1]
        without_localhost = without_protocol.split("/", 1)[1]
        return "/" + without_localhost


