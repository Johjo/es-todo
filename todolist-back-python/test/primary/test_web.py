import bottle  # type: ignore
import pytest
from approvaltests import verify  # type: ignore
from webtest import TestApp, TestResponse  # type: ignore

from hexagon.fvp.domain_model import ChooseTheTask
from test.primary.controller.read.test_which_task import DependencyListForTest, WhichTaskQueryForTest
from primary.web import app as bottle_app


@pytest.fixture
def which_task_query():
    return WhichTaskQueryForTest()


@pytest.fixture
def web_app(which_task_query):
    bottle.debug(True)
    bottle_app.dependencies = DependencyListForTest(which_task_query=which_task_query)
    return bottle_app


@pytest.fixture
def app(web_app):
    return TestApp(web_app)


def test_rest_which_task(app, which_task_query):
    which_task_query.feed(ChooseTheTask(id_1=1, name_1="buy the milk", id_2=2, name_2="clean the table"))

    try:
        response: TestResponse = app.get('/rest/todo/anytodolist/which_task')
    except Exception as e:
        print(e)
        raise

    assert response.status == '200 OK'
    verify(response.body)