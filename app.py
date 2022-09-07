from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1111@localhost:5432/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class GroupModel(db.Model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


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
