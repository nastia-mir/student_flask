from flask import request, jsonify
from flask_restful import Resource
from controllers.Controller import Controller


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
    def post(self):
        if not request.args or not 'name' in request.args or not 'surname' in request.args:
            return 404
        stud_name = request.args.get('name')
        stud_surname = request.args.get('surname')
        controller = Controller()
        controller.student_add(stud_name, stud_surname)
        result = dict()
        result['first_name'] = stud_name
        result['last_name'] = stud_surname
        result['action'] = 'added'
        api_data = controller.get_data(result)
        return jsonify(api_data)

    def delete(self):
        if not request.args or not 'id' in request.args:
            return 404
        stud_id = request.args.get('id')
        controller = Controller()
        controller.student_delete(stud_id)
        result = dict()
        result['id'] = stud_id
        result['action'] = 'deleted'
        api_data = controller.get_data(result)
        return jsonify(api_data)





