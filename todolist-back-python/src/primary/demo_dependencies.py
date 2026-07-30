import os
from pathlib import Path

from dotenv import load_dotenv

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort
from hexagon.todolist.port import TaskKeyGeneratorPort
from infra.memory import Memory
from primary.adapter_in_memory_dependencies import inject_adapter_in_memory
from primary.controller.read.final_version_perfected import CalendarPort
from primary.controller.use_case_dependencies import inject_use_cases
from primary.controller.write.todolist import DateTimeProviderPort
from primary.infrastructure_in_memory_dependencies import inject_infrastructure_in_memory
from secondary.calendar import Calendar
from secondary.datetime_provider import DateTimeProvider
from secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from infra.fvp_memory import FvpMemory
from secondary.todolist.task_key_generator_random import TaskKeyGeneratorRandom

memory = Memory()
fvp_memory = FvpMemory()

def inject_all_dependencies(dependencies: Dependencies) -> Dependencies:
    dependencies = inject_use_cases(dependencies)
    dependencies = inject_adapter_in_memory(dependencies)
    dependencies = inject_infrastructure_in_memory(dependencies=dependencies, memory=memory, fvp_memory=fvp_memory)

    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: TaskKeyGeneratorRandom())
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, DateTimeProvider.factory)
    dependencies = dependencies.feed_adapter(CalendarPort, Calendar.factory)
    load_dotenv()
    dependencies = dependencies.feed_path("static_path", lambda _: Path(os.environ["STATIC_PATH"]))
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)

    return dependencies


