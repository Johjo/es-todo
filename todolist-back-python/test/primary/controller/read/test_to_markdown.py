from hexagon.shared.type import TaskOpen
from primary.controller.read.todolist import to_markdown, Task
from test.fixture import TodolistFaker


def test_convert_no_task():
    assert to_markdown([]) == ""

def test_convert_one_task(fake: TodolistFaker):
    task = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(True)).to_task()
    assert to_markdown([task]) == f"- [ ] {task.name}"

def test_convert_many_tasks(fake: TodolistFaker):
    task_1 = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(True)).to_task()
    task_2 = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(True)).to_task()
    assert to_markdown([task_1, task_2]) == f"- [ ] {task_1.name}\n- [ ] {task_2.name}"

def test_convert_closed_task(fake: TodolistFaker):
    task = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(False)).to_task()
    assert to_markdown([task]) == f"- [x] {task.name}"



