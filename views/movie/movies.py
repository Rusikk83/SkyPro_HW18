# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

# Пример
from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie, movies_schema, movie_schema
from flask import request, Response
#
movies_ns = Namespace('movies')
#
#
@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        genre_id = request.args.get("genre_id")
        director_id = request.args.get("director_id")
        year = request.args.get("year")
        if year:
            books = db.session.query(Movie).filter(Movie.year == year)
        elif genre_id:
            books = db.session.query(Movie).filter(Movie.genre_id == genre_id)
        elif director_id:
            books = db.session.query(Movie).filter(Movie.director_id == director_id)
        else:
            books = db.session.query(Movie).all()
        return movies_schema.dump(books), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        print(new_movie.id)
        db.session.commit()
        print(new_movie.id)
        resp = Response(status=201)
        resp.headers['Location'] = f'http://127.0.0.1:5000/movies/{new_movie.id}'

        return resp


@movies_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == id).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, id):
        movie = db.session.query(Movie).get(id)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()


        return "", 204

    def patch(self, id):
        movie = db.session.query(Movie).get(id)
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, id):
        movie = db.session.query(Movie).get(id)

        db.session.delete(movie)
        db.session.commit()

        return "", 204
