from flask import Blueprint, render_template,flash,redirect,url_for,session
from ..core import db
from ..users.models import Group
from . import route
from ..users.forms import Group_Form

bp = Blueprint('dashboard', __name__)

@route(bp,'/submit/<id>', methods=('GET','POST'))
def submit_edit(id):
	form = Group_Form()

	if form.validate_on_submit():
		grp = Group.query.filter_by(id=id).first()
		grp.name = form.data['name']
		db.session.commit()
		
	return redirect(url_for('.index'))

@route(bp,'/submit', methods=('GET', 'POST') )
def submit():
	form = Group_Form()

	if form.validate_on_submit():
		ngroup = Group( )
		tmp = Group.query.filter_by(name=form.data['name']).first()
		if tmp is None :
			ngroup.name = form.data['name']
			db.session.add(ngroup)
			db.session.commit()
		else:
			flash('Grupo ya existe')

	return redirect(url_for('.index'))


@route(bp,'/<id>/del')
def del_group(id):
	grp = Group.query.filter_by( id = id).first()
	
	db.session.delete(grp)
	db.session.commit()
	return redirect(url_for('.index'))


@route(bp,'/<id>')
def show_group(id):
	grp = Group.query.filter_by(id=id).first()

	form = Group_Form( name=grp.name  )

	return render_template('show_group.html', form=form, grp=grp)


@route(bp, '/')
def index():
	g =  Group.query.all()
	form = Group_Form()	

	return render_template('grp_index.html', groups = g , form = form   )


