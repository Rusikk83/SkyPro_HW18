# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

from flask import Flask
from flask_restx import Api
#
from config import Config
from models import Movie, Genre, Director
from setup_db import db
from views.movie.movies import movies_ns
from views.genre.genre import genres_ns
from views.director.director import director_ns


# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(director_ns)


app = create_app(Config())  # создание приложения с параметрами конфигурации из класса config
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)  # старт приложения
