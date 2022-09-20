from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


student_course = Table('student_course',
                       Base.metadata,
                       Column('student_id', Integer, ForeignKey('student.id')),
                       Column('course_id', Integer, ForeignKey('course.id',)),
                       )


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    student = relationship("Student", back_populates="group")

    def __repr__(self):
        return "<Group(name='{})'>".format(self.name)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    group_id = Column(Integer, ForeignKey('group.id'))

    group = relationship("Group", back_populates="student")
    course = relationship('Course',
                          secondary=student_course,
                          back_populates='student',
                          #cascade="all, delete"
                          )

    def __repr__(self):
        return "<Student(first_name='{}', last_name='{}')>".format(self.first_name, self.last_name)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    student = relationship("Student",
                           secondary=student_course,
                           back_populates="course",
                           )

    def __repr__(self):
        return "<Course(name='{})'>".format(self.name)


engine = create_engine('postgresql://postgres:1111@localhost:5432/students')
if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
