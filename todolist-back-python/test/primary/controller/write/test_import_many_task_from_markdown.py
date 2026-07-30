
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.fixture import TodolistFaker, TaskBuilder
from test.primary.controller.write.conftest import TodolistSetForTest


def test_import_many_task_from_markdown(todolist_set: TodolistSetForTest, sut: TodolistWriteController, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    expected_tasks = [fake.a_task(1), fake.a_task(2)]
    markdown = markdown_from_tasks(expected_tasks)

    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    task_key_generator.feed(*[task for task in expected_tasks])

    sut.import_many_tasks_from_markdown(todolist.name, markdown)

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=expected_tasks).to_snapshot()


def markdown_from_tasks(expected_tasks: list[TaskBuilder]) -> str:
    return "\n".join([f"- [ ] {task.name}" for task in expected_tasks])


