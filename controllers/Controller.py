from models.Model import Group, Student, Course, Session, engine, student_course
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError

s = Session()


class Controller():
    def groups_leq_students(self, num):
        correct_group_names = []
        result = dict()
        groups = s.query(Group).group_by(Group.id).all()
        for group in groups:
            print(len(group.student))
        '''for i in range(1, 11):
            students_in_group = s.query(Student).join(Group).filter(Group.id == i)
            if students_in_group.count() <= num:
                for stud in students_in_group:
                    if stud.group.name not in correct_group_names:
                        correct_group_names.append(stud.group.name)'''
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

        stud = Student(first_name=stud_first_name, last_name=stud_last_name)
        s.add(stud)
        s.commit()

        result = dict()
        result['id'] = stud.id
        name = dict()
        name['first name'] = stud.first_name
        name['last name'] = stud.last_name
        result['name'] = name
        result['action'] = 'added'
        return result

    def student_delete(self, stud_id):
        if not stud_id:
            return {'error': 'wrong request'}
        student = s.query(Student).filter_by(id=stud_id).first()
        if not student:
            return {'error': 'no student with given id.'}
        s.delete(student)
        s.commit()

        result = dict()
        result['id'] = stud_id
        result['action'] = 'deleted'
        return result

    def add_student_to_course(self, stud_id, course_id):
        result = dict()
        try:
            statement = student_course.insert().values(student_id=stud_id, course_id=course_id)
            s.execute(statement)
            result['added'] = True
            result['student id'] = stud_id
            result['course id'] = course_id

        except IntegrityError:
            s.commit()
            result['added'] = False

        s.commit()
        return result

    def remove_student_from_course(self, stud_id, course_id):
        result = dict()
        try:
            statement = student_course.delete().where(student_course.c.student_id == stud_id,
                                                      student_course.c.course_id == course_id)
            s.execute(statement)
            result['deleted'] = True
            result['student id'] = stud_id
            result['course id'] = course_id

        except IntegrityError:
            s.commit()
            result['deleted'] = False

        s.commit()
        return result

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
            student_courses = [course.name for course in student.course]
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
            student_courses = [course.name for course in student.course]
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
            student_courses = [course.name for course in student.course]
            result['courses'] = student_courses
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
