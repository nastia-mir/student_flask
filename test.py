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


params_names = [{'first_name': 'Jonathan', 'last_name': 'Sims'},
                {'first_name': 'Martin', 'last_name': 'Sims'},
                {'first_name': 'Sasha', 'last_name': 'James'}]

params_wrong_requests = [{'name': 'somename', 'message': "wrong student name"},
                         {'name': 'Jonathan', 'message': "wrong student name"}]


def test_students(client):
    for name in params_names:
        response = client.get('/api/v1/students/?first_name={}&last_name={}'.format(name['first_name'],
                                                                                    name['last_name']))  # correct name
        assert response.json['name']['first name'] == name['first_name']
        assert response.json['name']['last name'] == name['last_name']

    for request in params_wrong_requests:
        response = client.get('/api/v1/students/?first_name={}&last_name={}'.format(request['name'],
                                                                                    request['name']))  # incorrect name
        assert response.json['message'] == request['message']

    response = client.get('/api/v1/students/?first_name=Jonathan')  # 1 argument given
    assert response.json['message'] == 'wrong request'

    response = client.get('/api/v1/students/')  # more than 1 student
    student_present = False
    for i in range(1, 201):
        if response.json['{}'.format(i)]:
            student_present = True
    assert student_present


params_courses = [{'id': '1', 'course_name': 'Mathematics'},
                  {'id': '2', 'course_name': 'Biology'},
                  {'id': '6', 'course_name': 'Literature'},
                  {'id': '8', 'course_name': 'History'}]


def test_courses(client):
    response = client.get('/api/v1/courses/')
    for course in params_courses:
        assert response.json[course['id']]['course name'] == course['course_name']


params_group = [{'id': '1', 'group_name': "PP-60"},
                {'id': '3', 'group_name': "PC-14"},
                {'id': '6', 'group_name': "NF-74"}]


def test_groups(client):
    response = client.get('/api/v1/groups/')
    for group in params_group:
        assert response.json[group['id']]['group name'] == group['group_name']


def test_groups_leq_studs(client):
    response = client.get('/api/v1/groups/?students=15')
    assert "ZG-87" in response.json['groups']


def test_studs_course(client):
    response = client.get('/api/v1/students/courses/?course=History')
    assert "Martin Cane", "Peter Robinson" in response.json['History']
    assert "Sasha James" not in response.json['History']


def test_student_add_delete(client):
    data_add = {
        "first_name": "Melanie",
        "last_name": "Sims"
    }
    url = '/api/v1/students/'
    response1_add = client.post(url, data=json.dumps(data_add))
    added_stud_id = response1_add.json['id']
    assert response1_add.json['name']['first name'] == "Melanie"
    assert response1_add.json['name']['last name'] == "Sims"
    response2_add = client.post(url, data=json.dumps(data_add))
    assert response2_add.json['message'] == "student already exists"

    data_delete = {
        "id": added_stud_id
    }
    response1_delete = client.delete(url, data=json.dumps(data_delete))
    assert response1_delete.json['action'] == 'deleted'
    assert response1_delete.json['id'] == added_stud_id
    response2_delete = client.delete(url, data=json.dumps(data_delete))
    assert response2_delete.json['message'] == "no student with given id"


def test_add_student_to_course(client):
    data1 = {
        "student_id": "200",
        "course_id": "9"
    }
    url = '/api/v1/students/courses/'
    response = client.post(url, data=json.dumps(data1))
    assert 'English' in response.json['courses']
    assert response.json['id'] == 200
    data2 = {
        "student_id": "220",
        "course_id": "9"
    }
    response = client.post(url, data=json.dumps(data2))
    assert response.json['message'] == 'wrong id'


def test_remove_student_from_course(client):
    data = {
        "student_id": "200",
        "course_id": "9"
    }
    url = '/api/v1/students/courses/'
    response = client.delete(url, data=json.dumps(data))
    assert response.json['deleted'] == True
    assert response.json['course id'] == '9'
    assert response.json['student id'] == '200'


def test_error_handler(client):
    response = client.get('api/v1/students/4')
    assert response.json['status'] == '404'
