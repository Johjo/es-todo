import pytest

from hexagon.query.context_query import OpenTaskReader, TodoContextQuery

# todo read step 4: introduce test around query
class SimpleOpenTaskReader(OpenTaskReader):
    def __init__(self):
        self._tasks = []

    def feed(self, *tasks):
        self._tasks.extend(tasks)

    def all(self):
        return self._tasks


@pytest.fixture
def task_reader():
    return SimpleOpenTaskReader()


@pytest.fixture
def sut(task_reader: SimpleOpenTaskReader) -> TodoContextQuery:
    return TodoContextQuery(task_reader)


def test_return_no_context_when_no_task(sut: TodoContextQuery):
    assert sut.all_contexts() == {}


@pytest.mark.parametrize("title, tasks, expected", [
    ("default", ["#context"], {"#context" : 1}),
    ("ignore text before", ["avant #context"], {"#context" : 1}),
    ("each word beginning by #", ["avant #other"], {"#other": 1}),
    ("accept words and symbol", ["avant #CoNtExt1_-"], {"#context1_-": 1}),
    ("ignore text after", ["avant #CoNtExt après"], {"#context" : 1}),
    ("task can have many contexts", ["#context1 #context2"], {"#context1" : 1, "#context2" : 1}),
    ("same context count as one", ["#context #context"], {"#context" : 1}),
    ("each task can have a context", ["#context1", "#context2"], {"#context1" : 1, "#context2" : 1}),
    ("sum tasks when in the same context", ["#context", "#context"], {"#context" : 2}),
    ("tasks can have same and different contexts", ["#context1 #context2", "#context1"], {"#context1" : 2, "#context2" : 1}),
    ("accept @ as context", ["#context1", "@context2"], {"#context1" : 1, "@context2" : 1}),
])
def test_return_context_from_task(sut: TodoContextQuery, task_reader: SimpleOpenTaskReader, title: str, tasks: list[str], expected: list[str]):
    task_reader.feed(*tasks)
    assert sut.all_contexts() == expected
