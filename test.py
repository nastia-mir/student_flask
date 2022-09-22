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


@pytest.mark.parametrize("correct_requests", [{'first_name': 'Jonathan', 'last_name': 'Sims'},
                                              {'first_name': 'Martin', 'last_name': 'Sims'},
                                              {'first_name': 'Sasha', 'last_name': 'James'}])
def test_students_correct_request(client, correct_requests):
    response = client.get('/api/v1/students/?first_name={}&last_name={}'.format(correct_requests['first_name'],
                                                                                correct_requests['last_name']))
    assert response.json['name']['first name'] == correct_requests['first_name']
    assert response.json['name']['last name'] == correct_requests['last_name']


@pytest.mark.parametrize("wrong_requests", [{'name': 'somename', 'message': "wrong student name"},
                                            {'name': 'Jonathan', 'message': "wrong student name"}])
def test_students_wrong_request(client, wrong_requests):
    response = client.get('/api/v1/students/?first_name={}&last_name={}'.format(wrong_requests['name'],
                                                                                wrong_requests['name']))
    assert response.json['message'] == wrong_requests['message']


def test_students_one_arg(client):
    response = client.get('/api/v1/students/?first_name=Jonathan')
    assert response.json['message'] == 'wrong request'


def test_all_students(client):
    response = client.get('/api/v1/students/')
    student_present = False
    for i in range(1, 201):
        if response.json['{}'.format(i)]:
            student_present = True
    assert student_present


@pytest.mark.parametrize("courses", [{'id': '1', 'course_name': 'Mathematics'},
                                     {'id': '2', 'course_name': 'Biology'},
                                     {'id': '6', 'course_name': 'Literature'},
                                     {'id': '8', 'course_name': 'History'}])
def test_courses(client, courses):
    response = client.get('/api/v1/courses/')
    assert response.json[courses['id']]['course name'] == courses['course_name']


@pytest.mark.parametrize("groups", [{'id': '1', 'group_name': "PP-60"},
                                    {'id': '3', 'group_name': "PC-14"},
                                    {'id': '6', 'group_name': "NF-74"}])
def test_groups(client, groups):
    response = client.get('/api/v1/groups/')
    assert response.json[groups['id']]['group name'] == groups['group_name']


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
