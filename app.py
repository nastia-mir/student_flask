from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.routes import data_bp, api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1111@localhost:5432/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views.view import GroupsLeqStudentsAPI, StudentsCourseAPI, StudentsAPI
from models.Model import Session

api.add_resource(GroupsLeqStudentsAPI, "/groups_leq_studs/", endpoint="/groups_leq_studs/")
api.add_resource(StudentsCourseAPI, "/studs_course/", endpoint="/studs_course/")
api.add_resource(StudentsAPI, "/students/", endpoint="/students/")
app.register_blueprint(data_bp, url_prefix="/api/v1")


@app.errorhandler(404)
def handle_404(e):
    return {"status": "404", "message": "Page not found"}


@app.errorhandler(500)
def handle_500(e):
    return {"status": "500", "message": "Something went wrong"}


@app.before_request
def before_request():
    s = Session()


@app.after_request
def after_request(response):
    #s.close()
    return response


if __name__ == "__main__":
    app.run(debug=True)






