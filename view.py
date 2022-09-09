from Model import Group, Student, Course, student_course, Session

s = Session()


def groups_leq_students(num):
    correct_groups_ids = []
    for i in range(1, 11):
        if s.query(Student).filter_by(group_id=i).count() <= num:
            correct_groups_ids.append(i)
    correct_group_names = []
    for id in correct_groups_ids:
        for group in s.query(Group).filter_by(id=id):
            correct_group_names.append(group.name)
    return correct_group_names


def students_related_to_course(course_name):
    for course in s.query(Course).filtered_dy(name=course_name):
        course_id = course






def student_add(stud_first_name, stud_last_name):
    stud = Student(first_name=stud_first_name, last_name=stud_last_name)
    s.add(stud)
    s.commit()


def student_delete(stud_id):
    student = s.query(Student).filter_by(id=stud_id).first()
    s.delete(student)
    s.commit()


def add_student_to_course(stud_id, course_id):
    for student in s.query(Student).filter_by(id=stud_id):
        for course in s.query(Course).filter_by(id=course_id):
            student.course.append(course)
            s.commit()


def remove_student_from_course(stud_id, course_id):
    for student in s.query(Student).filter_by(id=stud_id):
        for course in s.query(Course).filter_by(id=course_id):
            student.course.pop()

            #not working




remove_student_from_course(200,5)

s.close()
