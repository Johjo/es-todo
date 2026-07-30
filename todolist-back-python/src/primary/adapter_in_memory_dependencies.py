from hexagon.fvp.aggregate import FvpSessionSetPort
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.todolist.port import TodolistSetPort
from primary.controller.read.todolist import TodolistSetReadPort
from secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
from secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory


def inject_adapter_in_memory(dependencies):
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
    return dependencies
