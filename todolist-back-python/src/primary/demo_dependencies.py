import os
from pathlib import Path

from dotenv import load_dotenv

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSessionSetPort
from src.hexagon.fvp.read.which_task import TodolistPort
from src.hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from src.infra.memory import Memory
from src.primary.controller.read.final_version_perfected import CalendarPort
from src.primary.controller.read.todolist import TodolistSetReadPort
from src.primary.controller.use_case_dependencies import inject_use_cases
from src.primary.controller.write.todolist import DateTimeProviderPort
from src.secondary.calendar import Calendar
from src.secondary.datetime_provider import DateTimeProvider
from src.secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory
from src.secondary.todolist.task_key_generator_random import TaskKeyGeneratorRandom
from src.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory
from src.secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory
from src.shared.const import USER_KEY

memory = Memory()
fvp_session = FvpSessionSetInMemory()
def inject_all_dependencies(dependencies: Dependencies) -> Dependencies:
    dependencies = inject_use_cases(dependencies)
    dependencies = dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: TaskKeyGeneratorRandom())
    dependencies = dependencies.feed_adapter(TodolistPort, TodolistInMemory.factory)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, TodolistSetReadInMemory.factory)
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, DateTimeProvider.factory)
    dependencies = dependencies.feed_adapter(CalendarPort, Calendar.factory)
    dependencies = dependencies.feed_infrastructure(Memory, lambda _: memory)
    dependencies = dependencies.feed_data(USER_KEY, "user@mail.com")
    load_dotenv()
    dependencies = dependencies.feed_path("static_path", lambda _: Path(os.environ["STATIC_PATH"]))
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: fvp_session)

    return dependencies
