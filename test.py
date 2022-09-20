import flask
import pytest
import re
from app import app


@pytest.fixture()
def myapp():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(myapp):
    return app.test_client()


def find_str(text, word):
    result = re.search(word, text)
    return result


def test_students(client):
    response = client.get('/api/v1/students/?first_name=Jonathan&last_name=Sims')  # correct name
    assert find_str(str(response.data), '"first name": "Jonathan", "last name": "Sims"')
    assert not find_str(str(response.data), '"first name": "Melanie"')
    response = client.get('/api/v1/students/?first_name=somename&last_name=somename')  # incorrect name
    assert find_str(str(response.data), 'wrong student')
    response = client.get('/api/v1/students/?first_name=Jonathan')  # 1 argument given
    assert find_str(str(response.data), 'wrong request')
    response = client.get('/api/v1/students/')  # more than 1 student
    assert find_str(str(response.data), '"1":')
    assert find_str(str(response.data), '"5":')


def test_courses(client):
    response = client.get('/api/v1/courses/')
    assert find_str(str(response.data), '"course name": "Biology"')
    assert find_str(str(response.data), '"course name": "History"')


def test_groups(client):
    response = client.get('/api/v1/groups/')
    assert find_str(str(response.data), '"group name": "HP-20", "students": ["Jane Blackwood","Michael Tonner",')
    assert find_str(str(response.data), '"group name": "HJ-63", "students": ["Georgie Barker"')



def test_error_handler(client):
    response = client.get('api/v1/students/4')
    assert find_str(str(response.data), 'not found')
