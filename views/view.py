from flask import request, jsonify
from flask_restful import Resource
from controllers.Controller import Controller
import ast


class GroupsLeqStudentsAPI(Resource):
    def get(self):
        students_num = request.args.get('students')
        controller = Controller()
        api_data = controller.get_data(controller.groups_leq_students(students_num))
        return jsonify(api_data)


class StudentsCourseAPI(Resource):
    def get(self):
        course_name = request.args.get('course')
        controller = Controller()
        api_data = controller.get_data(controller.students_related_to_course(course_name))
        return jsonify(api_data)


class StudentsAPI(Resource):
    def get(self):
        controller = Controller()
        if not request.args or not 'first_name' in request.args or not 'last_name' in request.args:
            api_data = controller.get_data(controller.show_students)
        else:
            stud_first_name = request.args.get('first_name')
            stud_last_name = request.args.get('last_name')
            api_data = controller.get_data(controller.show_one_student(stud_first_name, stud_last_name))
        return jsonify(api_data)

    def post(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_first_name = data.get("first_name")
        stud_last_name = data.get("last_name")

        controller = Controller()
        adding = controller.student_add(stud_first_name, stud_last_name)

        if adding == {'error': 'wrong request'}:
            return jsonify(adding)

        result = dict()
        name = dict()
        name['first name'] = stud_first_name
        name['last name'] = stud_last_name
        result['name'] = name
        result['action'] = 'added'
        api_data = controller.get_data(result)
        return jsonify(api_data)

    def delete(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_id = data.get('id')

        controller = Controller()
        controller.student_delete(stud_id)

        result = dict()
        result['id'] = stud_id
        result['action'] = 'deleted'
        api_data = controller.get_data(result)
        return jsonify(api_data)


class CoursesAPI(Resource):
    def get(self):
        controller = Controller()
        api_data = controller.get_data(controller.show_courses())
        return jsonify(api_data)


class GroupAPI(Resource):
    def get(self):
        controller = Controller()
        api_data = controller.get_data(controller.show_groups())
        return jsonify(api_data)
