import flask
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import LoginManager
import os

#dbuser = movieslibapp
#db passwd movieslibapp_passwd
#url =   mongodb://<dbuser>:<dbpassword>@ds019976.mlab.com:19976/levimovies

MoviesLib_app = flask.Flask(__name__)
MoviesLib_app.config['MONGOALCHEMY_DATABASE'] = 'levimovies'
MoviesLib_app.config['MONGOALCHEMY_SERVER'] = 'ds019976.mlab.com'
MoviesLib_app.config['MONGOALCHEMY_PORT'] = '19976'
MoviesLib_app.config['MONGOALCHEMY_USER'] = 'movieslibapp'
MoviesLib_app.config['MONGOALCHEMY_PASSWORD'] = 'movieslibapp_passwd'
MoviesLib_app.config['MONGOALCHEMY_SERVER_AUTH'] = False
#MoviesLib_app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://movieslibapp:movieslibapp_passwd@ds01316.mlab.com:1316/levimovies'
#MoviesLib_app.config['DEBUG'] = True

db = MongoAlchemy(MoviesLib_app)
login_manager = LoginManager()
login_manager.init_app(MoviesLib_app)

import views
login_manager.login_view = views.login
_ = views
