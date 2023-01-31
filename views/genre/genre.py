from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie
from flask import request
#
genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return "", 200


@genres_ns.route('<int:id>')
class GenreView(Resource):
    def get(self, id):
        return "", 200
