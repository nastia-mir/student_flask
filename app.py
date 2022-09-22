from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.routes import data_bp, api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1111@localhost:5432/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from views.view import StudentsAPI, CoursesAPI, GroupAPI, StudentCourseAPI

api.add_resource(StudentsAPI, "/students/", endpoint="/students/")
api.add_resource(StudentCourseAPI, "/students/courses/", endpoint="/students/courses/")
api.add_resource(CoursesAPI, "/courses/", endpoint="/courses/")
api.add_resource(GroupAPI, "/groups/", endpoint="/groups/")
app.register_blueprint(data_bp, url_prefix="/api/v1")


@app.errorhandler(404)
def handle_404(e):
    return {"status": "404", "message": "Page not found"}


@app.errorhandler(500)
def handle_500(e):
    return {"status": "500", "message": "Something went wrong"}


if __name__ == "__main__":
    app.run(debug=True)






