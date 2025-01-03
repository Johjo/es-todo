from datetime import datetime

from src.hexagon.shared.type import TaskOpen
from src.primary.controller.read.todolist import to_markdown
from test.fixture import TodolistFaker


def test_convert_no_task():
    assert to_markdown([]) == ""

def test_convert_one_task(fake: TodolistFaker):
    task = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(True)).to_presentation()
    assert to_markdown([task]) == f"- [ ] {task.name}"


def test_convert_many_tasks_old(fake: TodolistFaker):
    task_1 = fake.a_task().having(name="task 1", is_open=TaskOpen(True)).to_presentation()
    task_2 = fake.a_task().having(name="task 2", is_open=TaskOpen(False), execution_date=datetime(2020, 6, 17).date()).to_presentation()
    task_3 = fake.a_task().having(name="task 3", is_open=TaskOpen(True)).to_presentation()
    assert to_markdown([task_1, task_2, task_3]) == "- [ ] task 1\n- [x] task 2{execution_date=2020-06-17}\n- [ ] task 3"


def test_convert_date(fake: TodolistFaker):
    task = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(True), execution_date=datetime(2022, 7, 13).date()).to_presentation()
    assert to_markdown([task]) == f"- [ ] {task.name}{{execution_date=2022-07-13}}"


def test_convert_closed_task(fake: TodolistFaker):
    task = fake.a_task().having(name=fake.task_name(), is_open=TaskOpen(False)).to_presentation()
    assert to_markdown([task]) == f"- [x] {task.name}"



