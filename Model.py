from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from app import db


class GroupModel(db.Model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))

    def __repr__(self):
        return "<GroupModel(name='{}'".format(self.name)


class StudentModel(db.Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship(GroupModel)


class CourseModel(db.Model):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))


engine = create_engine('postgresql://postgres:1111@localhost:5432/students')
if not database_exists(engine.url):
    create_database(engine.url)
db.Model.metadata.create_all(engine)


def recreate_database():
    db.Model.metadata.drop_all(engine)
    db.Model.metadata.create_all(engine)


recreate_database()