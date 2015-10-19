from ..core import db
from ..users.models import Group
from datetime import datetime

group_wp = db.Table(
	'wp_group',
	db.Column('wp_id', db.Integer(), db.ForeignKey('wp.id')),
	db.Column('group_id', db.Integer(), db.ForeignKey('group.id')))


tag_wp = db.Table(
	'wp_tag',
	db.Column('wp_id', db.Integer(), db.ForeignKey('wp.id')),
	db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')) 
	)

entity_entity = db.Table(
	'entity_relation',
	db.Column('parent_id', db.Integer(), db.ForeignKey('entity.id')),
	db.Column('child_id', db.Integer(), db.ForeignKey('entity.id')) 
	)


class Wp(db.Model):

	__tablename__ = 'wp'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True)
	order = db.Column(db.Integer)
	entities = db.relationship("Entity", backref="wp", lazy="dynamic")
	status = db.relationship('Status', backref="wp" , lazy="dynamic")
	groups = db.relationship('Group', secondary=group_wp,
							backref=db.backref('wps', lazy='dynamic'))
	tags = db.relationship('Tag', secondary=tag_wp,
							backref=db.backref('wpst', lazy='dynamic'))

	def __repr__(self):
		return "< Wp - %s " % (self.name )

#http://stackoverflow.com/questions/22203159/generate-a-dynamic-form-using-flask-wtf-and-sqlalchemy

class Field(db.Model):

	__tablename__='field'
	id = db.Column(db.Integer , primary_key=True)
	id_entity =  db.Column( db.Integer,  db.ForeignKey('entity.id'))
	type = db.Column( db.String(21) )
	name = db.Column(db.String(255))
	value = db.Column(db.String(255))

	def __init__(self, type , name , value):
		self.type = type
		self.name = name
		self.value = value	

	

class Entities_relations(db.Model):

	__tablename__ = 'entities_relations'
	id = db.Column(db.Integer, primary_key = True )
	id_parent = db.Column(db.Integer)
	id_child = db.Column(db.Integer)


class Entity(db.Model):

	__tablename__='entity'
	id = db.Column(db.Integer , primary_key=True)
	id_wp = db.Column(db.Integer , db.ForeignKey('wp.id') )
	name = db.Column( db.String(255) )
	etype = db.Column( db.String(12 )  )
	id_status =  db.Column( db.Integer,  db.ForeignKey('status.id'))
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	created_by = db.Column(db.String(255))
	updated_by = db.Column(db.String(255))
	fields = db.relationship('Field', backref="entity" , lazy="dynamic")
	childs = db.relationship('Entity',secondary=entity_entity , primaryjoin=id==entity_entity.c.parent_id , secondaryjoin=id==entity_entity.c.child_id,backref='entity_entity_ref')


	def __init__(self, id_wp, name, etype, id_status,created_at = None):
		
		self.id_wp = id_wp
		self.name = name
		self.etype = etype
		self.id_status = id_status

		if created_at is None:
			self.created_at = datetime.utcnow()


class Status(db.Model):

	__tablename__='status'
	id = db.Column(db.Integer, primary_key=True )
	id_wp = db.Column(db.Integer,  db.ForeignKey('wp.id'))
	etype = db.Column(db.String(12))
	name = db.Column(db.String(255))
	nextStatus = db.Column( db.Integer )

	def __repr__(self):
		return "< %s,Status - %s >" % ( self.id ,self.name ) 


class Tag(db.Model):

	__tablename__='tag'
	id = db.Column(db.Integer, primary_key=True)
	id_wp = db.Column(db.Integer,  db.ForeignKey('wp.id'))
	name = db.Column(db.String(120))


