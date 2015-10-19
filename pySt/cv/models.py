from ..core import db


class Skill(db.Model):
	__bind_key__ = 'cv'
	id = db.Column(db.Integer, primary_key = True )
	name = db.Column(db.String(80), unique=True)
	nivel = db.Column(db.String(90))
	category_id =  db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',
		backref=db.backref('skills', lazy='dynamic'))

	def __init__(self,category_id,name,nivel):
		self.category_id = category_id
		self.name = name
		self.nivel = nivel

	def __repr__(self):
		return "<Skill %s>" % self.name

class Category(db.Model):
	__bind_key__ = 'cv'
	id = db.Column(db.Integer, primary_key = True )
	name = db.Column(db.String(80), unique = True )
	order = db.Column(db.Integer)

	def __init__(self, name , order ):
		self.name = name
		self.order = order

	def __repr__(self):
		return "<Category %s %s >" % (self.name , self.order)



class Laboral(db.Model):
	__bind_key__ = 'cv'
	id = db.Column(db.Integer, primary_key=True )
	company = db.Column( db.String(90))
	start = db.Column(db.DateTime)
	end = db.Column(db.DateTime)

	def __init__(self, company , start , end ):
		self.company = company
		self.start = start
		self.end = end

	def __repr__(self):
		return "<Laboral %s" % self.company


