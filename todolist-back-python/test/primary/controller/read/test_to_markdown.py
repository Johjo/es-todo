from hexagon.shared.type import TaskOpen
from primary.controller.read.todolist import to_markdown, Task
from test.fixture import TodolistFaker


def test_convert_no_task():
    assert to_markdown([]) == ""

def test_convert_one_task(fake: TodolistFaker):
    task = Task(id=fake.task_key(), name=fake.task_name(), is_open=TaskOpen(True))
    assert to_markdown([task]) == f"- [ ] {task.name}"

def test_convert_many_tasks(fake: TodolistFaker):
    task_1 = Task(id=fake.task_key(), name=fake.task_name(), is_open=TaskOpen(True))
    task_2 = Task(id=fake.task_key(), name=fake.task_name(), is_open=TaskOpen(True))
    assert to_markdown([task_1, task_2]) == f"- [ ] {task_1.name}\n- [ ] {task_2.name}"

def test_convert_closed_task(fake: TodolistFaker):
    task = Task(id=fake.task_key(), name=fake.task_name(), is_open=TaskOpen(False))
    assert to_markdown([task]) == f"- [x] {task.name}"



