import pytest
from expression import Option, Some, Nothing

from src.dependencies import Dependencies
from src.hexagon.todolist.aggregate import TodolistSnapshot
from src.hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from src.infra.fvp_memory import FvpMemory
from src.infra.memory import Memory
from src.primary.adapter_in_memory_dependencies import inject_adapter_in_memory
from src.primary.controller.use_case_dependencies import inject_use_cases
from src.primary.controller.write.todolist import TodolistWriteController, DateTimeProviderPort
from src.primary.infrastructure_in_memory_dependencies import inject_infrastructure_in_memory
from src.shared.const import USER_KEY
from test.fixture import TodolistBuilder
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest, DateTimeProviderForTest
from test.primary.controller.conftest import memory


class TodolistSetForTest(TodolistSetPort):
    def __init__(self) -> None:
        self._all_todolist: dict[str, Option[TodolistSnapshot]] = {}

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_todolist:
            raise Exception("todolist must be fed before being read")

        return self._all_todolist[todolist_name]

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._all_todolist[todolist.name] = Some(todolist)

    def feed(self, todolist: TodolistSnapshot | TodolistBuilder) -> None:
        if isinstance(todolist, TodolistSnapshot):
            self._all_todolist[todolist.name] = Some(todolist)
        if isinstance(todolist, TodolistBuilder):
            self._all_todolist[todolist.name] = Some(todolist.to_snapshot())

    def feed_with_nothing(self, todolist_name: str) -> None:
        self._all_todolist[todolist_name] = Nothing


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()

@pytest.fixture
def dependencies(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                 datetime_provider: DateTimeProviderForTest, memory: Memory, fvp_memory: FvpMemory) -> Dependencies:
    dependencies = inject_use_cases(Dependencies.create_empty())
    dependencies = inject_adapter_in_memory(dependencies)
    dependencies = inject_infrastructure_in_memory(dependencies=dependencies, memory=memory, fvp_memory=fvp_memory)
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(DateTimeProviderPort, lambda _: datetime_provider)
    dependencies = dependencies.feed_data(data_name=USER_KEY, value="any user")

    return dependencies

@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorForTest:
    return TaskKeyGeneratorForTest()


@pytest.fixture
def datetime_provider() -> DateTimeProviderForTest:
    return DateTimeProviderForTest()


@pytest.fixture
def sut(dependencies: Dependencies) -> TodolistWriteController:
    return TodolistWriteController(dependencies)