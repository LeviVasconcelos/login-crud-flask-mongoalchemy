import flask
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from movieslib.likeapi import LikeAPI


import os

#dbuser = movieslibapp
#db passwd movieslibapp_passwd
#url =   mongodb://<dbuser>:<dbpassword>@ds019976.mlab.com:19976/levimovies

MoviesLib_app = flask.Flask(__name__)
MoviesLib_app.config['MONGOALCHEMY_DATABASE'] = 'levimovies'
MoviesLib_app.config['MONGOALCHEMY_SERVER'] = 'ds019976.mlab.com'
MoviesLib_app.config['MONGOALCHEMY_PORT'] = '19976'
MoviesLib_app.config['MONGOALCHEMY_USER'] = os.environ['MONGOLAB_USER'] 
MoviesLib_app.config['MONGOALCHEMY_PASSWORD'] = os.environ['MONGOLAB_PASSWD'] 
MoviesLib_app.config['MONGOALCHEMY_SERVER_AUTH'] = False
MoviesLib_app.config['SECRET_KEY']= os.environ['FORM_SKEY'] 
#MoviesLib_app.config['DEBUG'] = True

db = MongoAlchemy(MoviesLib_app)


login_manager = LoginManager()
login_manager.init_app(MoviesLib_app)

import views
from movieslib.documents import Movie, User

login_manager.login_view = views.login

like_api_view = LikeAPI.as_view('like_movie', collection=Movie, user_col=User)
MoviesLib_app.add_url_rule('/movies/like/<id>', view_func=like_api_view, methods=['GET'])

_ = views
