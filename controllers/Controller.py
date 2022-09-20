from models.Model import Group, Student, Course, Session

s = Session()


class Controller():
    def groups_leq_students(self, num):
        correct_group_names = []
        result = dict()
        for i in range(1, 11):
            students_in_group = s.query(Student).join(Group).filter(Group.id == i)
            if students_in_group.count() <= num:
                for stud in students_in_group:
                    if stud.group.name not in correct_group_names:
                        correct_group_names.append(stud.group.name)
        result['groups'] = correct_group_names
        return result

    def students_related_to_course(self, course_name):
        query = s.query(Student).join(Course.student)
        students_on_course = []
        result = dict()
        for row in query:
            for course in row.course:
                if course.name == course_name:
                    students_on_course.append(' '.join([row.first_name, row.last_name]))
        result[course_name] = students_on_course
        return result

    def student_add(self, stud_first_name, stud_last_name):
        student = s.query(Student).filter_by(first_name=stud_first_name, last_name=stud_last_name).first()

        if student:
            return {'error': 'student already exists.'}
        elif not stud_first_name or not stud_last_name:
            return {'error': 'wrong request'}

        last_stud = s.query(Student).order_by(Student.id.desc()).first()
        stud = Student(id=last_stud.id + 1, first_name=stud_first_name, last_name=stud_last_name)
        s.add(stud)
        s.commit()

    def student_delete(self, stud_id):
        if not stud_id:
            return {'error': 'wrong request'}
        student = s.query(Student).filter_by(id=stud_id).first()
        if not student:
            return {'error': 'no student with given id.'}
        s.delete(student)
        s.commit()

    def add_student_to_course(self, stud_id, course_id):
        for student in s.query(Student).filter_by(id=stud_id):
            if not student:
                return {"error": "wrong student id."}
            for course in s.query(Course).filter_by(id=course_id):
                if not course:
                    return {"error": "wrong course id."}
                student.course.append(course)
                s.commit()

    def remove_student_from_course(self, stud_id, course_id):
        for student in s.query(Student).filter_by(id=stud_id):
            deleted = False
            if not student:
                return {"error": "wrong student id."}
            for course in student.course:
                if course.id == course_id:
                    deleted = True
                    student.course.pop()
                    s.commit()
        return {"deleted": deleted}

    def get_data(self, lst):
        return {'data': lst}

    def show_students(self):
        result = dict()
        for student in s.query(Student):
            student_info = dict()
            stud_name = dict()
            stud_name['first name'] = student.first_name
            stud_name['last name'] = student.last_name
            student_info['name'] = stud_name
            if not student.group:
                student_info['group name'] = 'None'
            else:
                student_info['group name'] = student.group.name
            student_courses = []
            query = s.query(Student).join(Course.student)
            for row in query:
                for course in row.course:
                    if row.id == student.id:
                        student_courses.append(course.name)
            student_info['courses'] = student_courses
            result[student.id] = student_info
        return result

    def show_one_student(self, first_name, last_name):
        student = s.query(Student).filter_by(first_name=first_name, last_name=last_name).first()
        if not student:
            return {'error': 'wrong student name'}
        else:
            result = dict()
            student_info = dict()
            stud_name = dict()
            stud_name['first name'] = first_name
            stud_name['last name'] = last_name
            student_info['name'] = stud_name
            if not student.group:
                student_info['group name'] = 'None'
            else:
                student_info['group name'] = student.group.name
            student_courses = []
            query = s.query(Student).join(Course.student)
            for row in query:
                for course in row.course:
                    if row.id == student.id:
                        student_courses.append(course.name)
            student_info['courses'] = student_courses
            result[student.id] = student_info
        return result

    def show_courses(self):
        result = dict()
        for course in s.query(Course):
            course_info = dict()
            course_info['course name'] = course.name
            course_info['description'] = course.description
            result[course.id] = course_info
        return result

    def show_courses_of_one_student(self, stud_id):
        student = s.query(Student).filter_by(id=stud_id).first()
        if not student:
            return {'error': 'wrong student id'}
        else:
            result = dict()
            stud_name = dict()
            stud_name['first name'] = student.first_name
            stud_name['last name'] = student.last_name
            result['name'] = stud_name
            result['id'] = student.id
            student_courses = []
            query = s.query(Student).join(Course.student)
            if query:
                for row in query:
                    for course in row.course:
                        if row.id == stud_id:
                            student_courses.append(course.name)
                result['courses'] = student_courses
            else:
                result['courses'] = 'None'
        return result

    def show_groups(self):
        result = dict()
        for group in s.query(Group):
            group_info = dict()
            group_info['group name'] = group.name
            studs = []
            for stud in group.student:
                studs.append(' '.join([stud.first_name, stud.last_name]))
            group_info['students'] = studs
            result[group.id] = group_info
        return result


s.close()
