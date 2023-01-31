from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie
from flask import request
#
director_ns = Namespace('directors')


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        return "", 200


@director_ns.route('/<int:id>')
class DirctorView(Resource):
    def get(self, id):
        return "", 200