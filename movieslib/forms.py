import wtforms
from flask.ext import wtf
from wtforms import validators

from documents import Movie, User

class MovieAddForm(wtf.Form):
	document_class = Movie
	title = wtforms.TextField(validators=[validators.Required(message='Title field required.'), validators.Length(min=1,max=100, message='title must be between 1 and 100 characters')])
	year = wtforms.IntegerField(validators=[validators.Required(message='Year Field required.'), validators.NumberRange(min=1900,max=2020, message='Year should be between 1900 and 2020')])
	synopse = wtforms.TextAreaField()

	related_doc = None

	def __init__(self, doc=None, *argc, **kwargs):
		super(MovieAddForm, self).__init__(*argc,**kwargs)
		if doc:
			self.related_doc = doc
			self._fill_form()

	def _fill_form(self):
		self.title.data = self.related_doc.title
		self.year.data = self.related_doc.year
		self.synopse.data = self.related_doc.synopse

	def save_to_db(self):
		if self.related_doc is None:
			self.related_doc = self.document_class()
		self.related_doc.title = self.title.data
		self.related_doc.year = self.year.data
		self.related_doc.synopse = self.synopse.data
		self.related_doc.likes_users = []
		self.related_doc.save()
		return self.related_doc

import bcrypt

def ColUnique(collection, collection_field, message='This entry already exists on dataset'):
	def _unique(form, field):
		doc = collection.query.filter({collection_field:field.data}).first()
		if doc:
			raise validators.ValidationError(message)
	return _unique

def Exists(collection, collection_field, message='This entry does not exists on dataset'):
	def _exists(form, field):
		doc = collection.query.filter({collection_field:field.data}).first()
		print doc
		if not doc:
			raise validators.ValidationError(message)
	return _exists


class LoginForm(wtf.Form):
	username = wtforms.TextField(validators=[validators.Required(message='Login field required.'), Exists(User, 'username', message='Invalid username.')])
	passwd = wtforms.PasswordField(validators=[validators.Required(message='Password field required.'), validators.Length(min=8, message='Password most be more than 8 characters long.')])

	related_usr = None

	def __init__(self, *argc, **kwargs):
		super(LoginForm, self).__init__(*argc,**kwargs)

	def read_form(self):
		if related_usr is None:
			related_usr = User()
		related_usr.username = self.username.data
		related_usr.passwd = self.username.passwd


class SignUpForm(wtf.Form):
	username = wtforms.TextField('Username', validators=[validators.Required(message='Username required.'), ColUnique(User, 'username', message='This username already exists.')])
	passwd = wtforms.PasswordField('Password', validators=[validators.Required(message='Password field required.'), validators.Length(min=8, message='Your password must be at least 8 characters long.')])
	passwd_check = wtforms.PasswordField('Repeat password', validators=[validators.Required(),  validators.EqualTo('passwd', message='Passwords must check.')])
	email = wtforms.TextField('Email Address', validators=[validators.Required(message='Email field required.'), validators.Email(message='Not a valid email address'), ColUnique(User,'email',message='This email is already registered.')])

	related_usr = None

	def __init__(self, *argc, **kwargs):
		super(SignUpForm, self).__init__(*argc,**kwargs)


	def save_to_db(self, group=None):
		if group is None:
			return
		if self.related_usr is None:
			self.related_usr = User()
		self.related_usr.username = self.username.data
		self.related_usr.passwd = bcrypt.hashpw(self.passwd.data.encode('utf-8'), bcrypt.gensalt())
		self.related_usr.email = self.email.data
		self.related_usr.perms = set([group])
		self.related_usr.authenticated = 0
		self.related_usr.save()	



