import flask
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import LoginManager


MoviesLib_app = flask.Flask(__name__)
MoviesLib_app.config['MONGOALCHEMY_DATABASE'] = 'movies'
MoviesLib_app.config['SECRET_KEY'] = 'try out'
#MoviesLib_app.config['DEBUG'] = True

db = MongoAlchemy(MoviesLib_app)
login_manager = LoginManager()
login_manager.init_app(MoviesLib_app)

import views
login_manager.login_view = views.login
_ = views
