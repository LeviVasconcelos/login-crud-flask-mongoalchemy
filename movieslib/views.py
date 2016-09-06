from flask import render_template, url_for, redirect, request, session
from movieslib import MoviesLib_app, login_manager
from forms import MovieAddForm, LoginForm, SignUpForm
from documents import Movie, User
from flask.ext.login import login_required, login_user, logout_user, current_user
from functools import wraps
import bcrypt

'''
Decorator to check for user permissions.
'''
def has_perm(perm, fail_view):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
        	allow = True
        	for p in perm:
        		allow = (allow and (p in current_user.perms))
        	if (allow):
        		return f(*args, **kwargs)
        	return redirect(url_for(fail_view))
        return decorated_function
    return decorator



@login_manager.user_loader
def load_user(usrname):
	usr = User.query.filter({'username':usrname}).first()
	if usr:
		return usr
	return None

@MoviesLib_app.route('/')
def start(): 
	return redirect(url_for('list_movies'))


@MoviesLib_app.route('/movies')
@MoviesLib_app.route('/movies/<int:page>')
@login_required
def list_movies(page=1):
	title = u'Movies library'
	order = session.get('order_by', None)
	movies_page = Movie.query.get_ordered(order=order).paginate(page=page,per_page = 5)
	return render_template('lib/paging_all.html',title=title, movies_page=movies_page, order=order, page=page)


@MoviesLib_app.route('/movies', methods=['POST'])
@MoviesLib_app.route('/movies/<int>', methods=['POST'])
@login_required
def switch_order():
	session['order_by'] = request.form['order_by']
	return redirect(url_for('list_movies'))


@MoviesLib_app.route('/movies/add')
@login_required
def new_movie():
	title = u'Add a Movie'
	form = MovieAddForm()
	return render_template('lib/add.html',form=form,title=title)


@MoviesLib_app.route('/movies/add', methods=['POST'])
@login_required
def add_movie():
	form = MovieAddForm()
	if form.validate_on_submit():
		form.save_to_db()
		return redirect(url_for('list_movies',page=1))
	return render_template('lib/add.html',form=form)


@MoviesLib_app.route('/movies/edit/<id>', methods=['GET','POST'])
@login_required
@has_perm(['admin'], fail_view='list_movies')
def movie_edit(id):
	page = request.args.get('page',1)
	mv = Movie.query.get(id)
	form = MovieAddForm()
	if form.validate_on_submit():
		form.related_doc = mv
		form.save_to_db()
		return redirect(url_for('list_movies',page=page))
	form = MovieAddForm(mv)
	return render_template('lib/edit.html',form=form)


@MoviesLib_app.route('/movies/detail/<id>')
@login_required
def movie_detail(id):
	page = request.args.get('page',1)
	mv = Movie.query.get(id)
	return render_template('lib/detail.html',movie=mv,page=page)


@MoviesLib_app.route('/movies/delete/<id>')
@login_required
@has_perm(['admin'], fail_view='list_movies')
def movie_delete(id):
	mv = Movie.query.get_or_404(id)
	mv.remove()
	page = int(request.args.get('page',1))
	page_obj = Movie.query.get_ordered().paginate(page=page,per_page=5)
	if page_obj.items is None:
		page = 1
	return redirect(url_for('list_movies',page=page))




##############################################################################################################################################################
##############################################################################################################################################################



@MoviesLib_app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		usr = User.query.filter({'username': form.username.data}).first()
		if bcrypt.hashpw(form.passwd.data.encode('utf-8'), usr.passwd.encode('utf-8')) == usr.passwd.encode('utf-8'):
			usr.authenticated = 1
			usr.save()
			login_user(usr)
			return redirect(url_for('list_movies'))
	return render_template('login/login.html', form=form)

@MoviesLib_app.route('/sign_up', methods=['GET','POST'])
def sign_up():
	form = SignUpForm()
	if form.validate_on_submit():
		group = request.form.get('perm',None)
		if group is None:
			return 'None group'
		form.save_to_db(group)
		return redirect('login')
	return render_template('login/signup.html',form=form)

@MoviesLib_app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))


	
