from flask import Blueprint
from flask_restful import Api

data_bp = Blueprint('user_bp', __name__)
api = Api(data_bp)

data_bp.route("/groups_leq_studs/", methods=['GET'])
data_bp.route("/studs_course/", methods=['GET'])
data_bp.route("/students/", methods=['GET', 'POST', 'DELETE'])
data_bp.route("/students/courses/", methods=['GET', 'POST', 'DELETE'])
data_bp.route("/courses/", methods=['GET'])
data_bp.route("/groups/", methods=['GET'])
