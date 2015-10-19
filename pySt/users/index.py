from flask import request,Blueprint, render_template,flash,redirect,url_for,session
from ..core import db
from . import route
from ..users.models import User,Group
from ..users.forms import User_Form

bp = Blueprint('dashboard', __name__)


@route(bp,'/submit/<id>', methods=('GET','POST'))
def submit_edit(id):
	form = User_Form()
	grps = Group.query.all()

	choices = [( str(x.id), x.name) for x in grps]
	form.groups.choices = choices
	if form.validate_on_submit():
		user = User.query.filter_by(id=id).first()
		user.username = form.data['username']
		user.password = form.data['password']
		user.active = True

		user.groups = []
		db.session.commit()

		grps = Group.query.filter( Group.id.in_(form.data['groups']) ).all()

		for grp in grps:
			user.groups.append(grp)

		db.session.commit()

	return redirect(url_for('.index'))


@route(bp,'/submit', methods=('GET', 'POST') )
def submit():
	form = User_Form()
	grps =  Group.query.all()

	choices = [( str(x.id), x.name) for x in grps]

	form.groups.choices = choices
	

	if form.validate_on_submit():

		nuser = User( )

		tmp = User.query.filter_by(username=form.data['username']).first()
		
		if tmp is None :
			nuser.username = form.data['username']
			nuser.password = form.data['password']
			nuser.active = True 

			#Add groups
			grps = Group.query.filter( Group.id.in_(form.data['groups']) ).all()

			for grp in grps:
				nuser.groups.append(grp)
			
			db.session.add(nuser)
			db.session.commit()

		else:
			flash('Usuario ya existe')
	else:
		flash(form.errors)
		
	return redirect(url_for('.index'))


@route(bp,'/<id_user>/del')
def del_user(id_user):
	user = User.query.filter_by( id = id_user).first()
	
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('.index'))


@route(bp, '/<id_user>')
def show_user(id_user):
	
	user = User.query.filter_by(id=id_user).first()

	
#http://stackoverflow.com/questions/5519729/wtforms-how-to-select-options-in-selectmultiplefield
	grps =  Group.query.all()

	choices = [( str(x.id), x.name) for x in grps]

	default = [  x.id  for x in user.groups  ]

	form = User_Form(    )

	form.username.default=user.username

	form.groups.default = default

	form.groups.choices = choices

	form.process()

	return render_template('show_user.html', form=form, user=user)


@route(bp, '/')
def index():
	form = User_Form()

	user =  User.query.all()

	grps =  Group.query.all()

	choices = [( str(x.id), x.name) for x in grps]

	form.groups.choices = choices
	

	"""Returns the dashboard interface."""
	return render_template('user_index.html',form=form ,grps=grps, users= user  )