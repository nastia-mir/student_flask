import json
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
    assert find_str(str(response.data), '"first name": "Jonathan"')
    assert find_str(str(response.data), '"last name": "Sims"')
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
    assert find_str(str(response.data), '"group name": "PP-60"')
    assert find_str(str(response.data), '"group name": "EX-90"')


def test_groups_leq_studs(client):
    response = client.get('/api/v1/groups_leq_studs/?students=16')
    assert find_str(str(response.data), '"PP-60"')
    assert find_str(str(response.data), '"PP-60"')


def test_studs_course(client):
    response = client.get('/api/v1/studs_course/?course=History')
    assert find_str(str(response.data), '"Martin Cane"')
    assert find_str(str(response.data), '"Peter Robinson"')


def test_student_add(client):
    data = {
        "first_name": "Melanie",
        "last_name": "Sims"
    }
    url = '/api/v1/students/'
    response1 = client.post(url, data=json.dumps(data))
    assert response1.json['data']['name']['first name'] == "Melanie"
    assert response1.json['data']['name']['last name'] == "Sims"
    response2 = client.post(url, data=json.dumps(data))
    assert response2.json['error'] == "student already exists."


def test_student_delete(client):
    data = {
        "id": 201
    }
    url = '/api/v1/students/'
    response1 = client.delete(url, data=json.dumps(data))
    assert response1.json['data']['action'] == 'deleted'
    assert response1.json['data']['id'] == 201
    response2 = client.delete(url, data=json.dumps(data))
    assert response2.json['error'] == "no student with given id."


def test_add_student_to_course(client):
    data1 = {
        "student_id": "200",
        "course_id": "9"
    }
    url = '/api/v1/students/courses/'
    response = client.post(url, data=json.dumps(data1))
    assert 'English' in response.json['data']['courses']
    assert response.json['data']['id'] == 200
    data2 = {
        "student_id": "220",
        "course_id": "9"
    }
    response = client.post(url, data=json.dumps(data2))
    assert response.json['data']['error'] == 'wrong student id'


def test_remove_student_from_course(client):
    data = {
        "student_id": "200",
        "course_id": "9"
    }
    url = '/api/v1/students/courses/'
    response1 = client.delete(url, data=json.dumps(data))
    assert response1.json['data']['action'] == 'deleted'
    assert response1.json['data']['course_id'] == '9'
    assert response1.json['data']['student_id'] == '200'
    response2 = client.delete(url, data=json.dumps(data))
    assert response2.json['error'] == 'student do not attend given course.'


def test_error_handler(client):
    response = client.get('api/v1/students/4')
    assert find_str(str(response.data), 'not found')
