from flask import request,Blueprint, render_template,flash,redirect,url_for,session
from ..core import db
from . import route
from ..users.models import User,Group
from ..wp.models import Wp,Tag,Status
from ..wp.forms import Wp_Status_Form,Wp_Form,Wp_grps_Form,Wp_tags_Form


bp = Blueprint('dashboard', __name__)


@route(bp,'/<id_wp>/status/<type>/<id>/del')
def delete_status(id_wp,type,id):
	st = Status.query.get(id)

	db.session.delete(st)
	db.session.commit()

	return redirect(url_for('.status_type', type=type , id_wp=id_wp))


@route(bp, '/<id_wp>/status/submit_status')
def submit_status(id_wp):

	return redirect(url_for('.status',id_wp=id_wp))


@route(bp,'/<id_wp>/status/<type>')
def status_type(id_wp,type):
	form = Wp_Status_Form( id_wp =id_wp )

	wp = Wp.query.get(id_wp)

	status = Status.query.filter_by( etype = type ).all()

	return render_template('list_status.html',type=type, status=status,form=form, wp=wp)


@route(bp,'/<id_wp>/status' , methods=('GET','POST') )
def status(id_wp):
	form = Wp_Status_Form( id_wp =id_wp )

	if Wp_Status_Form.validate_on_submit:
		s = Status()
		s.name =  form.data['name']
		s.etype = form.data['etype']
		s.id_wp = id_wp

		db.session.add(s)
		db.session.commit()

	wp = Wp.query.get(id_wp)

	etype = request.form['etype']

	return redirect(url_for('.status_type', type=etype , id_wp=id_wp))


@route(bp,'/submit/<id_wp>/tags', methods=('GET','POST'))
def submit_edit_tags(id_wp):
	form = Wp_tags_Form()

	if form.validate_on_submit():
		tag = Tag()
		tmp = Tag.query.filter_by( name = form.data['name']).first()
		if tmp is None:
			tag.name = form.data['name']
			tag.id_wp = form.data['id_wp']

			db.session.add(tag)

			db.session.commit()
		else:
			flash("tag ya existe")

	else:
		flash(form.errors)

	return redirect(url_for('.show_wp',id_wp=id_wp))


@route(bp,'/submit/<id_wp>/grps',methods=('GET','POST'))
def submit_edit_grps(id_wp):
	form = Wp_grps_Form()
	grps =  Group.query.all()
	choices = [( str(x.id), x.name) for x in grps]
	form.groups.choices = choices

	if form.validate_on_submit():
		wp = Wp.query.filter_by(id=id_wp).first()
		wp.groups = []

		db.session.commit()
		#Add groups
		grps = Group.query.filter( Group.id.in_(form.data['groups']) ).all()

		for grp in grps:
			wp.groups.append(grp)

		db.session.commit()

	return redirect(url_for('.show_wp',id_wp=id_wp))


@route(bp,'/submit/<id_wp>',  methods=('GET', 'POST') )
def submit_edit(id_wp):

	form = Wp_Form()
	if form.validate_on_submit():
		wp = Wp.query.filter_by(id=id_wp).first()
		wp.name = form.data['name']
		db.session.commit()

	return redirect(url_for('.index'))


@route(bp,'/submit', methods=('GET', 'POST'))
def submit():

	form = Wp_Form()
	if form.validate_on_submit():
		n_wp = Wp( )
		tmp = Wp.query.filter_by(name=form.data['name']).first()
		if tmp is None :
			n_wp.name = form.data['name']
			db.session.add(n_wp)
			db.session.commit()
		else:
			flash("Ya existe un wp")

	return redirect(url_for('.index'))


@route(bp,'/<id_wp>/del')
def del_wp(id_wp):
	wp = Wp.query.filter_by( id = id_wp).first()
	
	db.session.delete(wp)
	db.session.commit()

	return redirect(url_for('.index'))


@route(bp,'/<id_wp>')
def show_wp(id_wp):
	wp = Wp.query.filter_by(id=id_wp).first()

	form = Wp_Form( name=wp.name  )
	grps =  Group.query.all()

	choices = [( str(x.id), x.name) for x in grps]

	default = [  x.id  for x in wp.groups  ]


	form_grps = Wp_grps_Form()

	form_grps.groups.choices = choices
	form_grps.groups.default = default

	form_grps.process()

	tags_Form = Wp_tags_Form(id_wp=id_wp)

	tagsT = Tag.query.filter_by( id_wp=id_wp ).all()

	status_form = Wp_Status_Form( id_wp =id_wp )

	status_by_wp = Status.query.filter_by(id_wp=id_wp).group_by(Status.etype).order_by(Status.etype.asc()).order_by(Status.name.asc()).all()


	return render_template('show_wp.html',status_by_wp=status_by_wp,status_form=status_form, tagsT=tagsT,tags_Form=tags_Form, form_grps=form_grps, form=form, wp=wp)


@route(bp, '/')
def index():

	form = Wp_Form()
	wps = Wp.query.all()

	return render_template('wp_index.html', wps = wps , form=form )
