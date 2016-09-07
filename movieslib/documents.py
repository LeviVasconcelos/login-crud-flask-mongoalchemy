from movieslib import db
from flask_mongoalchemy import BaseQuery, fields





class User(db.Document):
	username = db.StringField()
	passwd = db.StringField(min_length=8)
	perms = db.SetField(db.StringField())
	email = db.StringField()

	authenticated = db.IntField(min_value=0, max_value=1)
	anonymous = False


	def is_authenticated(self):
		return 1 if self.authenticated else 0

	def is_active(self):
		return True

	def is_anonymous(self):
		return self.anonymous

	def get_id(self):
		return self.username


class MovieQueries(BaseQuery):

	def get_ordered(self, order = None):
		field = 'title' if order is None else order
		return self.ascending(field)


class Movie(db.Document):
	query_class = MovieQueries
	title = db.StringField(min_length = 1, max_length = 100)
	year = db.IntField(min_value = 1900, max_value = 2020)
	synopse = db.StringField(min_length = 1)
	likes_users = db.ListField(db.DocumentField(User))

	@fields.computed_field(db.IntField(), deps=[likes_users])
	def likes_count(usrs=[likes_users]):
		return len(usrs['likes_users'])







