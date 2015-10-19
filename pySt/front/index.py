from flask import session,flash,url_for,redirect,request,Blueprint, render_template
from ..core import db
from . import route
from ..users.models import User,Group
from ..cv.models import Skill,Category,Laboral
from ..wp.models import Wp,Tag,Status,Entity,Field,Entities_relations
from .forms import New_Folder_Form,New_Phase_Form,New_Contact_Form,New_Account_Form,New_Task_Form,New_Proyect_Form,Searh_Form,New_Client_Form,New_Note_Form
from datetime import datetime
import sys,inspect

bp = Blueprint('dashboard', __name__)

def get_classes():
    classes = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes[name] = obj
    return classes


def get_form( **kwargs ):
	form = None

	classes = get_classes()
	name_ = "New_"+ kwargs['etype'].capitalize() +"_Form"
	
	form = classes[name_]( **kwargs )

	return form


@route(bp,'/add_relation/<id_parent>/<id_child>')
def add_relation(id_parent,id_child):
	parent = Entity.query.get(id_parent)
	child = Entity.query.get(id_child)
	parent.childs.append(child)
	db.session.commit()

	return 'ok'

 
@route(bp,'/submit/<etype>', methods=('GET','POST'))
def submit_new_entity(etype):
	id_wp = request.values.get('id_wp')
	wp = Wp.query.all()
	status = Status.query.filter_by(etype=etype).filter_by(id_wp = id_wp ) .all()
	
	form = get_form( id_wp=id_wp , etype=etype)
	
	choices = [( str(x.id), x.name) for x in status]
	form.status.choices = choices

	if form.validate_on_submit():
		id_entity = request.values.get('id',False)

		if id_entity:
			en = Entity.query.get(id_entity)
			form.populate_obj(en)
			en.fields= []
			db.session.commit()

		else:
			en = Entity(id_wp, form.data['name'], etype, form.data['status'])
		
		if etype == 'client':
			# Call get_template( id_wp, etype )
			en.fields.append( Field("string",'first_name', form.data['first_name']))
			en.fields.append( Field("string",'last_name', form.data['last_name']))
			en.fields.append( Field("string",'email', form.data['email']))
			en.fields.append( Field("string",'address', form.data['address']))
			en.fields.append( Field("string",'site', form.data['site']))
			en.fields.append( Field("string",'phone', form.data['phone']))
			

		if etype == 'note':
			en.fields.append( Field("multilinestring",'note', form.data['note']))

		if etype == 'contact':
			en.fields.append( Field("string",'email', form.data['email']))
			en.fields.append( Field("string",'phone', form.data['phone']))
			en.fields.append( Field("string",'position', form.data['position']))

		if etype == 'phase':
			en.fields.append( Field("string",'phase', form.data['phase']))
			en.fields.append( Field("string",'type', form.data['type']))
			en.fields.append( Field("string",'owner', form.data['owner']))
			en.fields.append( Field("datetime",'planned_date_start', form.data['planned_date_start']))
			en.fields.append( Field("datetime",'planned_date_end', form.data['planned_date_end']))
			en.fields.append( Field("datetime",'real_date_start', form.data['real_date_start']))
			en.fields.append( Field("datetime",'real_date_end', form.data['real_date_end']))
			en.fields.append( Field("string",'name_proyect', form.data['name_proyect']))
			en.fields.append( Field("string",'tags', form.data['tags']))
			en.fields.append( Field("string",'snippet', form.data['snippet']))
			en.fields.append( Field("string",'goals', form.data['goals']))
			en.fields.append( Field("string",'budget', form.data['budget']))


		if not id_entity:
			db.session.add(en)

		id_parent = request.values.get('id_parent',False)
		
		if id_parent :
			p = Entity.query.get(id_parent)
			p.childs.append(en)

		db.session.commit()
	else:
		for field, errors in form.errors.items():
			for error in errors:
				flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
			
		return render_template('new_entity.html',etype=etype,form=form, wp=wp)

	return redirect(url_for('.index'))


@route(bp,'/del/<id>')
def del_entity(id):
	e = Entity.query.get(id)

	for f in e.fields.all():
		db.session.delete(f)
		

	db.session.delete(e)
	db.session.commit()
	return redirect(url_for('.index'))


@route(bp,'/show/<etype>/<id>')
def show_entity(etype,id):

	e = Entity.query.get(id)

	types = Status.query.filter_by(id_wp=e.id_wp).group_by(Status.etype).order_by(Status.etype.asc()).order_by(Status.name.asc()).all()

	return render_template('show_entity.html',  types=types , e=e)


@route(bp,'/edit/<etype>/<id>')
def edit_entity(etype,id):
	wp = Wp.query
	status = None
	id_wp = request.values.get('id_wp', None)
	if id_wp is not None:
		wp = wp.filter_by( id = id_wp )
		status = Status.query.filter_by( etype=etype).filter_by(id_wp = id_wp ).all()
	
	id_parent = request.values.get('id_parent',False)
	en = Entity.query.get(id)
	merge = en.__dict__

	for f in en.fields.all():

		if f.type == 'datetime':
			date_object = datetime.strptime(f.value, '%Y-%m-%d %H:%M:%S')
			tmp = { f.name : date_object }
		else:
			tmp = { f.name : f.value}
		print tmp
		merge.update( tmp )

	form = get_form( **merge  )

	print merge
 
	choices = [( str(x.id), x.name) for x in status]

	form.status.choices = choices

	wp = wp.all()

	return render_template('new_entity.html' ,etype=etype, en=en,id_parent=id_parent,form=form, wp=wp)


@route(bp,'/new/<etype>')
def new_entity(etype):
	wp = Wp.query
	status = None
	id_wp = request.values.get('id_wp', None)
	if id_wp is not None:
		wp = wp.filter_by( id = id_wp )
		status = Status.query.filter_by( etype=etype).filter_by(id_wp = id_wp ).all()
	
	id_parent = request.values.get('id_parent',False)

	form = get_form(id_wp = id_wp , etype = etype)

	choices = [( str(x.id), x.name) for x in status]

	form.status.choices = choices

	wp = wp.all()


	return render_template('new_entity.html' ,etype=etype, id_parent=id_parent,form=form, wp=wp)


@route(bp,'/client/<id>')
def show_client(id):

	client = Entity.query.get(id)
	wp  = Wp.query.get(client.id_wp)


	return render_template('show_client.html', wp=wp, client=client)


@route(bp,'/install')
def install():

	db.create_all()
	db.create_all(bind='cv')

	return 'ok'


@route(bp, '/',methods=('GET','POST'))
def index():
	entities =  Entity.query
	form = Searh_Form()
	status = []
	wps = Wp.query.all()
	choicesTags = [ ]
	tags = None

	if form.data:

		filter_wps = request.values.get('wps', None)
		if ( filter_wps != "all") & ( not filter_wps is  None   ):
			
			id_wp = form.data['wps']
			tags = Tag.query.filter_by( id_wp = id_wp ).all()
			choicesTags = [ ( str(x.id), x.name) for x in tags]
			status = Status.query.filter_by(id_wp = id_wp).group_by(Status.etype).order_by(Status.etype.asc()).order_by(Status.name.asc()).all()
			entities =  entities.filter_by(id_wp=id_wp)
			types = Entity.query.filter_by(id_wp=id_wp).group_by('etype').all()
			choices = [ (str(x.etype) , x.etype ) for x in types ]
			choices.append(('all','all'))
			choices.reverse()
			form.type.choices = choices

		filter_type = request.values.get('type', None)
		if ( filter_type != 'all') & ( not filter_type is None):
			etype = form.data['type']
			entities =  entities.filter_by(etype=etype)

		filter_q = request.values.get('type', None)
		if ( filter_q is not "" ) & (filter_q is not None):
			q = form.data['q']
			entities = entities.filter( Entity.name.like("%"+q+"%"))

	wps = Wp.query.all()
	choices = [ ( str(x.id), x.name) for x in wps]
	choices.append(   ('all','all')  )
	choices.reverse()
	
	choicesTags.append(( 'all','all' ) )
	choicesTags.reverse()

	form.tags.choices =choicesTags
	form.wps.choices = choices

	entities =  entities.all()
	
	"""Returns the dashboard interface."""
	return render_template('index.html', status=status,form=form , entities= entities  )