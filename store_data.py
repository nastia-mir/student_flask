import string
import random
import itertools
from Model import Group, Student, Course, Session


s = Session()


def generate_groups():
    for i in range(10):
        group_chars = [''.join(random.choice(string.ascii_uppercase)for n in range(2)), '-',
                       ''.join(random.choice(string.digits) for n in range(2))]
        group_name = ''.join(group_chars)
        group = Group(name=group_name)

        s.add(group)
        s.commit()


def generate_courses():
    course = Course(name='Mathematics', description='The science of numbers and shapes and what they mean.')
    s.add(course)
    s.commit()

    course = Course(name='Biology', description='The science that deals with living organisms and their vital '
                                                     'processes.')
    s.add(course)
    s.commit()

    course = Course(name='Chemistry', description='The science that deals with the properties, composition, '
                                                       'and structure of elements and compounds.')
    s.add(course)
    s.commit()

    course = Course(name='Geography', description='The study of places and the relationships between people and '
                                                       'their environments.')
    s.add(course)
    s.commit()

    course = Course(name='Physics', description='The science that deals with the structure of matter and how the '
                                                     'fundamental constituents of the universe interact.')
    s.add(course)
    s.commit()

    course = Course(name='Literature', description='Students read and respond to a variety of literary texts '
                                                        'from the genres of prose, poetry and drama.')
    s.add(course)
    s.commit()

    course = Course(name='Programming', description='Course include basic concepts in abstraction, algorithms, '
                                                         'operating systems and data structures.')
    s.add(course)
    s.commit()

    course = Course(name='History', description='The study of the past.')
    s.add(course)
    s.commit()

    course = Course(name='English', description='Students will study how to to speak, read and write in English.')
    s.add(course)
    s.commit()

    course = Course(name='Art', description='Course with a primary focus on the visual arts.')
    s.add(course)
    s.commit()


def generate_students():
    names = ['Monica', 'Andrew', 'Nicolas', 'Charlie', 'Dara', 'Rid', 'Robert', 'Natan', 'Enis', 'Melanie',
             'Anissa', 'Rafael', 'Alex', 'Patrick', 'Victor', 'Sean', 'Nelie', 'Kaycee', 'Justin', 'Daniel']
    surnames = ['Amos', 'Nelson', 'Spring', 'Alias', 'Potter', 'Lew', 'Dun', 'Beauchamp', 'Lonis', 'Kodish',
                'Polo', 'Heaton', 'Nedelec', 'Rice', 'Bloom', 'Clark', 'Byrne', 'Rien', 'Alien', 'Joseph']

    students = random.sample(set(itertools.product(names, surnames)), 200)
    for student in students:
        stud = Student(first_name=student[0], last_name=student[1])
        s.add(stud)
        s.commit()


    '''groups = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}

    for student in students:
        r = random.randint(1, 10)
        groups[r].append(student)

    groups_without_students = []
    for i in range(1, 10):
        if len(groups[i]) < 10 or len(groups[i]) > 30:
            groups['_'] = groups[i]
            groups_without_students.append(i)
            del groups[i]

    for i in range(1, 10):
        if i not in groups_without_students:
            for student in groups[i]:
                stud = Student(first_name=student[0], last_name=student[1])
                s.add(stud)
                s.commit()
    for student in groups['_']:
        stud = Student(first_name=student[0], last_name=student[1])
        s.add(stud)
        s.commit()'''


generate_groups()
generate_courses()
generate_students()


s.close()
