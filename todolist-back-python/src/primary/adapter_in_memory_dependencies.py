from src.hexagon.fvp.aggregate import FvpSessionSetPort
from src.hexagon.fvp.read.which_task import TodolistPort
from src.hexagon.todolist.port import TodolistSetPort
from src.primary.controller.read.todolist import TodolistSetReadPort
from src.secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
from src.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from src.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from src.secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory


def inject_adapter_in_memory(dependencies):
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
    return dependencies
