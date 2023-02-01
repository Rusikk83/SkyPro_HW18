from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie, movies_schema, movie_schema
from flask import request, Response

"""Создаем неймспейс для фильмов"""
movies_ns = Namespace('movies')

"""Представление для фильмов"""


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        """получение фильмов"""
        genre_id = request.args.get("genre_id")  # получаем id жанра из запроса
        director_id = request.args.get("director_id")  # получем id директора из запроса
        year = request.args.get("year")  # получаем id фильма из запроса
        if year:
            movies = db.session.query(Movie).filter(Movie.year == year)  # выбор фильмов с фильтром по году
        elif genre_id:
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id)  # выбор фильмов с фильтром по жанру
        elif director_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id)  # выбор фильмов по режиссеру
        else:
            movies = db.session.query(Movie).all()  # выбор всех фильмов
        return movies_schema.dump(movies), 200

    def post(self):
        """добавление фильма"""
        req_json = request.json  # получем атрибуты нового фильма из запроса
        new_movie = Movie(**req_json)  # создаем новый фильм
        db.session.add(new_movie)  # записываем новый фильм в БД
        db.session.commit()
        resp = Response(status=201)
        resp.headers['Location'] = f'http://127.0.0.1:5000/movies/{new_movie.id}'  # добавляем в ответ ссылку на фильм

        return resp


"""представление для получения, обновления, измнения и удаления фильма по id"""
@movies_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id):
        """получение фильма по id"""
        try:
            movie = db.session.query(Movie).filter(Movie.id == id).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, id):
        """обновление фильма по id"""
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
        """изменение фильма по id"""
        movie = db.session.query(Movie).get(id)
        req_json = request.json

        # изменяем только те атрибуты, которые есть в запросе
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
        """удаление фильма по id"""
        movie = db.session.query(Movie).get(id)

        db.session.delete(movie)
        db.session.commit()

        return "", 204
