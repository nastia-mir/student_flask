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
                    students_on_course.append([row.first_name, row.last_name])
        result[course_name] = students_on_course
        return result

    def student_add(self, stud_first_name, stud_last_name):
        stud = Student(first_name=stud_first_name, last_name=stud_last_name)
        s.add(stud)
        s.commit()

    def student_delete(self, stud_id):
        student = s.query(Student).filter_by(id=stud_id).first()
        s.delete(student)
        s.commit()

    def add_student_to_course(self, stud_id, course_id):
        for student in s.query(Student).filter_by(id=stud_id):
            for course in s.query(Course).filter_by(id=course_id):
                student.course.append(course)
                s.commit()

    def remove_student_from_course(self, stud_id, course_id):
        for student in s.query(Student).filter_by(id=stud_id):
            for course in student.course:
                if course.id == course_id:
                    student.course.pop()
                    print(student.course)
                    s.commit()

    def get_data(self, list):
        return {'data': list}

s.close()
