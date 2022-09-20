from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app import db


student_course = db.Table('student_course',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id', ondelete="CASCADE")),
                          db.Column('course_id', db.Integer, db.ForeignKey('course.id',  ondelete="CASCADE")),
                          #db.PrimaryKeyConstraint('student_id', 'course_id'),
                          extend_existing=True
                          )


class Group(db.Model):
    __tablename__ = 'group'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    student = relationship("Student", back_populates="group")

    def __repr__(self):
        return "<Group(name='{})'>".format(self.name)


class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    group_id = Column(Integer, ForeignKey('group.id'))

    group = relationship("Group", back_populates="student")
    #courses = relationship('Course', secondary=student_course, backref='student')
    course = relationship('Course',
                          secondary=student_course,
                          back_populates='student',
                          cascade="all, delete")

    def __repr__(self):
        return "<Student(first_name='{}', last_name='{}')>".format(self.first_name, self.last_name)


class Course(db.Model):
    __tablename__ = 'course'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    student = relationship("Student",
                           secondary=student_course,
                           back_populates="course",
                           #passive_deletes=True,
                           )

    def __repr__(self):
        return "<Course(name='{})'>".format(self.name)


engine = create_engine('postgresql://postgres:1111@localhost:5432/students')
if not database_exists(engine.url):
    create_database(engine.url)
db.Model.metadata.create_all(engine)


def recreate_database():
    db.Model.metadata.drop_all(engine)
    db.Model.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
