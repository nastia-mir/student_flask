from flask import request, jsonify
from flask_restful import Resource
from controllers.Controller import Controller
import ast


class StudentsAPI(Resource):
    def get(self):
        controller = Controller()
        if not request.args:
            api_data = controller.show_students()
        elif not 'first_name' in request.args or not 'last_name' in request.args:
            api_data = {"error": "wrong request"}
        else:
            stud_first_name = request.args.get('first_name')
            stud_last_name = request.args.get('last_name')
            api_data = controller.show_one_student(stud_first_name, stud_last_name)
        return jsonify(api_data)

    def post(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_first_name = data.get("first_name")
        stud_last_name = data.get("last_name")
        controller = Controller()
        result = controller.student_add(stud_first_name, stud_last_name)
        return jsonify(result)

    def delete(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_id = data.get('id')

        controller = Controller()
        result = controller.student_delete(stud_id)
        return jsonify(result)


class CoursesAPI(Resource):
    def get(self):
        controller = Controller()
        api_data = controller.show_courses()
        return jsonify(api_data)


class StudentCourseAPI(Resource):
    def get(self):
        controller = Controller()
        if 'course' in request.args:
            course_name = request.args.get('course')
            api_data = controller.students_related_to_course(course_name)
        elif 'student_id' in request.args:
            stud_id = request.args.get('student_id')
            api_data = controller.show_courses_of_one_student(int(stud_id))
        elif not request.args:
            return jsonify({'error': 'specify arguments'})

        return jsonify(api_data)

    def post(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_id = data.get("student_id")
        course_id = data.get("course_id")

        controller = Controller()
        adding = controller.add_student_to_course(stud_id, course_id)
        if adding['added']:
            api_data = controller.show_courses_of_one_student(int(stud_id))
            return jsonify(api_data)
        else:
            return jsonify({'error': 'wrong id'})

    def delete(self):
        data = ast.literal_eval(request.data.decode('utf-8'))
        stud_id = data.get("student_id")
        course_id = data.get("course_id")
        controller = Controller()
        delete = controller.remove_student_from_course(stud_id, course_id)

        if delete['deleted']:
            return jsonify(delete)
        else:
            return jsonify({'error': 'wrong id'})


class GroupAPI(Resource):
    def get(self):
        controller = Controller()
        students_num = request.args.get('students')
        if students_num:
            api_data = controller.groups_leq_students(int(students_num))
        else:
            api_data = controller.show_groups()
        return jsonify(api_data)
