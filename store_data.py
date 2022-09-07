import string
import random
from crud import Session
from Model import GroupModel, StudentModel, CourseModel


s = Session()


def generate_groups():
    for i in range(10):
        group_chars = [''.join(random.choice(string.ascii_uppercase)for n in range(2)), '-',
                       ''.join(random.choice(string.digits) for n in range(2))]
        group_name = ''.join(group_chars)
        group = GroupModel(name=group_name)

        s.add(group)
        s.commit()


def generate_courses():
    course = CourseModel(name='Mathematics', description='The science of numbers and shapes and what they mean.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Biology', description='The science that deals with living organisms and their vital '
                                                     'processes.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Chemistry', description='The science that deals with the properties, composition, '
                                                       'and structure of elements and compounds.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Geography', description='The study of places and the relationships between people and '
                                                       'their environments.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Physics', description='The science that deals with the structure of matter and how the '
                                                     'fundamental constituents of the universe interact.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Literature', description='Students read and respond to a variety of literary texts '
                                                        'from the genres of prose, poetry and drama.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Programming', description='Course include basic concepts in abstraction, algorithms, '
                                                         'operating systems and data structures.')
    s.add(course)
    s.commit()

    course = CourseModel(name='History', description='The study of the past.')
    s.add(course)
    s.commit()

    course = CourseModel(name='English', description='Students will study how to to speak, read and write in English.')
    s.add(course)
    s.commit()

    course = CourseModel(name='Art', description='Course with a primary focus on the visual arts.')
    s.add(course)
    s.commit()




generate_groups()
generate_courses()


s.close()