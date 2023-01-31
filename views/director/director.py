from flask_restx import Resource, Namespace
from setup_db import db
from models import Director, directors_schema, director_schema
from flask import request
#
director_ns = Namespace('directors')


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 200


@director_ns.route('/<int:id>')
class DirctorView(Resource):
    def get(self, id):
        try:
            director = db.session.query(Director).filter(Director.id == id).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404
