from flask_restx import Resource, Namespace
from setup_db import db
from models import Genre, genre_schema, genres_schema
from flask import request
#
genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == id).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404
