from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class GroupModel(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship(GroupModel)


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))


engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)